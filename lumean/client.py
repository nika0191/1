"""Client for the Lumean public API (https://api.lumean.app/api/public).

Covers the TTS path: find/create a voice template, create an order,
poll it to completion, and download the resulting audio file.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Iterable

import requests

DEFAULT_BASE_URL = "https://api.lumean.app/api/public"

TERMINAL_STATUSES = {
    "completed",
    "result_delivered",
    "failed",
    "compensated",
    "cancelled",
}
# partially_completed is intentionally excluded: it can be advanced to
# completed via retry-failed, so callers may want to act on it before giving up.


class LumeanAPIError(Exception):
    """Raised for any non-2xx response from the Lumean API."""

    def __init__(self, status_code: int, message: str, payload: dict | None = None):
        super().__init__(f"Lumean API error {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.payload = payload or {}


class PaygTopupRequired(LumeanAPIError):
    """402 payg_topup_required: subscription quota exhausted, PAYG top-up needed."""

    def __init__(self, status_code: int, message: str, payload: dict):
        super().__init__(status_code, message, payload)
        self.shortfall_tokens = payload.get("shortfall_tokens")
        self.shortfall_lmc = payload.get("shortfall_lmc")
        self.shortfall_lmc_minor = payload.get("shortfall_lmc_minor")
        self.quote_token = payload.get("quote_token")
        self.expires_at = payload.get("expires_at")


class QuoteMismatch(LumeanAPIError):
    """409 quote_mismatch: the PAYG top-up price changed, quote_token is stale."""


class TokenQuotaExceeded(LumeanAPIError):
    """429 with reason=token_quota_exceeded."""

    def __init__(self, status_code: int, message: str, payload: dict):
        super().__init__(status_code, message, payload)
        self.window = payload.get("window")
        self.limit = payload.get("limit")
        self.used = payload.get("used")
        self.requested = payload.get("requested")
        self.reset_at = payload.get("reset_at")
        self.retry_after = payload.get("retry_after")


class RateLimitExceeded(LumeanAPIError):
    """429 without a token-quota body (plain request-rate limiting)."""


def _raise_for_response(resp: requests.Response) -> None:
    if resp.ok:
        return
    try:
        payload = resp.json()
    except ValueError:
        payload = {}
    message = payload.get("message", resp.text or resp.reason)
    reason = payload.get("reason")

    if resp.status_code == 402 and reason == "payg_topup_required":
        raise PaygTopupRequired(resp.status_code, message, payload)
    if resp.status_code == 409 and reason == "quote_mismatch":
        raise QuoteMismatch(resp.status_code, message, payload)
    if resp.status_code == 429:
        if reason == "token_quota_exceeded":
            raise TokenQuotaExceeded(resp.status_code, message, payload)
        raise RateLimitExceeded(resp.status_code, message, payload)
    if resp.status_code == 422 and "errors" in payload:
        details = "; ".join(
            f"{field}: {', '.join(msgs)}" for field, msgs in payload["errors"].items()
        )
        raise LumeanAPIError(resp.status_code, f"{message} ({details})", payload)

    raise LumeanAPIError(resp.status_code, message, payload)


class LumeanClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        session: requests.Session | None = None,
    ):
        self.api_key = api_key or os.environ.get("LUMEAN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Lumean API key is required: pass api_key= or set LUMEAN_API_KEY"
            )
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def _headers(self) -> dict:
        return {"X-API-KEY": self.api_key}

    def _request(self, method: str, path: str, **kwargs) -> dict:
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        headers.update(self._headers())
        resp = self.session.request(
            method, url, headers=headers, timeout=self.timeout, **kwargs
        )
        _raise_for_response(resp)
        if not resp.content:
            return {}
        return resp.json()

    # ---- Voices ------------------------------------------------------

    def list_elevenlabs_voices(
        self,
        search: str | None = None,
        page: int = 0,
        page_size: int = 30,
        language_code: str | None = None,
        gender: str | None = None,
        age: str | None = None,
        accent: str | None = None,
    ) -> dict:
        params = {"page": page, "page_size": page_size}
        if search:
            params["search"] = search
        if language_code:
            params["required_languages"] = language_code
        if gender:
            params["gender"] = gender
        if age:
            params["age"] = age
        if accent:
            params["accent"] = accent
        body = self._request("GET", "/voices/elevenlabs/library", params=params)
        return body.get("data", {})

    # ---- Templates -----------------------------------------------------

    def browse_templates(
        self, service: str | None = None, page: int = 1, per_page: int = 100
    ) -> dict:
        params = {"page": page, "per_page": per_page}
        if service:
            params["service"] = service
        body = self._request("GET", "/templates/browse", params=params)
        return body.get("data", {})

    def create_template(
        self,
        service_key: str,
        name: str,
        config: dict,
        is_public: bool = False,
        folder_id: str | None = None,
    ) -> dict:
        payload = {
            "service_key": service_key,
            "name": name,
            "config": config,
            "is_public": is_public,
        }
        if folder_id:
            payload["folder_id"] = folder_id
        body = self._request("POST", "/templates", json=payload)
        return body["data"]

    def find_or_create_tts_template(
        self,
        voice_id: str,
        model_id: str = "eleven_multilingual_v2",
        language_code: str | None = None,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        style: float | None = None,
        use_speaker_boost: bool = True,
        speed: float = 1.0,
        advanced_voice_settings: bool = True,
        service_key: str = "elevenlabs",
    ) -> str:
        """Return an existing matching template's id, or create a new one."""
        browse = self.browse_templates(service=service_key, per_page=100)
        for item in browse.get("items", []):
            if item.get("type") != "template":
                continue
            tts = (item.get("config") or {}).get("tts_settings", {})
            if tts.get("voice_id") == voice_id and tts.get("model_id") == model_id:
                if language_code is None or tts.get("language_code") == language_code:
                    return item["id"]

        voice_settings = {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "use_speaker_boost": use_speaker_boost,
            "speed": speed,
        }
        if style is not None:
            voice_settings["style"] = style

        tts_settings = {
            "mode": "mode_v1",
            "model_id": model_id,
            "voice_id": voice_id,
            "advanced_voice_settings": advanced_voice_settings,
            "voice_settings": voice_settings,
        }
        if language_code:
            tts_settings["language_code"] = language_code

        template = self.create_template(
            service_key=service_key,
            name=f"auto-tts-{voice_id[:8]}-{model_id}",
            config={"tts_settings": tts_settings},
        )
        return template["id"]

    # ---- Orders --------------------------------------------------------

    def create_order(
        self,
        template_id: str | None = None,
        task_type: str | None = None,
        input_text: str | None = None,
        task_data: dict | None = None,
        config_override: dict | None = None,
        name: str | None = None,
        confirm_payg_topup: bool | None = None,
        quote_token: str | None = None,
    ) -> dict:
        payload: dict[str, Any] = {}
        if template_id:
            payload["template_id"] = template_id
        if task_type:
            payload["task_type"] = task_type
        if input_text is not None:
            payload["input_text"] = input_text
        if task_data is not None:
            payload["task_data"] = task_data
        if config_override is not None:
            payload["config_override"] = config_override
        if name:
            payload["name"] = name
        if confirm_payg_topup is not None:
            payload["confirm_payg_topup"] = confirm_payg_topup
        if quote_token:
            payload["quote_token"] = quote_token

        body = self._request("POST", "/orders", json=payload)
        return body["data"]

    def get_order(self, order_id: str) -> dict:
        body = self._request("GET", f"/orders/{order_id}")
        return body["data"]

    def cancel_order(self, order_id: str) -> dict:
        body = self._request("POST", f"/orders/{order_id}/cancel")
        return body["data"]

    def retry_failed_items(self, order_id: str) -> dict:
        body = self._request("POST", f"/orders/{order_id}/items/retry-failed")
        return body["data"]

    def retry_item(self, order_id: str, item_id: str, text: str | None = None) -> dict:
        payload = {"text": text} if text is not None else {}
        body = self._request(
            "POST", f"/orders/{order_id}/items/{item_id}/retry", json=payload
        )
        return body["data"]

    def wait_for_order(
        self,
        order_id: str,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
        stop_statuses: Iterable[str] = TERMINAL_STATUSES,
    ) -> dict:
        deadline = time.monotonic() + timeout
        while True:
            order = self.get_order(order_id)
            if order["status"] in stop_statuses:
                return order
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Order {order_id} did not reach a terminal status within "
                    f"{timeout}s (last status: {order['status']})"
                )
            time.sleep(poll_interval)

    # ---- Storage ---------------------------------------------------------

    def get_storage_url(
        self,
        path: str,
        download: bool = False,
        number_base: int | None = None,
        number_padding: int | None = None,
    ) -> str:
        payload: dict[str, Any] = {"path": path, "download": download}
        if number_base is not None:
            payload["number_base"] = number_base
        if number_padding is not None:
            payload["number_padding"] = number_padding
        body = self._request("POST", "/storage/url", json=payload)
        return body["data"]["url"]

    def download_file(self, path: str, out_path: str | Path) -> Path:
        url = self.get_storage_url(path)
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with self.session.get(url, stream=True, timeout=self.timeout) as resp:
            resp.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    f.write(chunk)
        return out_path

    # ---- Usage / subscriptions --------------------------------------------

    def get_usage(self) -> list[dict]:
        body = self._request("GET", "/usage")
        return body["data"]

    def get_subscriptions(self) -> dict:
        body = self._request("GET", "/subscriptions")
        return body["data"]

    # ---- High-level: text -> speech file -----------------------------------

    def synthesize_speech(
        self,
        text: str,
        out_path: str | Path,
        voice_id: str | None = None,
        template_id: str | None = None,
        model_id: str = "eleven_multilingual_v2",
        language_code: str | None = None,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        style: float | None = None,
        use_speaker_boost: bool = True,
        speed: float = 1.0,
        advanced_voice_settings: bool = True,
        download_subtitles: bool = False,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
        confirm_payg_topup: bool = False,
    ) -> dict:
        """Generate speech for `text` and save it to `out_path`.

        Either `template_id` or `voice_id` must be given. With `voice_id`,
        a matching template is reused or created automatically.
        Returns a dict with order_id, status, audio_path, and subtitle_paths.
        """
        if not template_id:
            if not voice_id:
                raise ValueError("Either template_id or voice_id is required")
            template_id = self.find_or_create_tts_template(
                voice_id=voice_id,
                model_id=model_id,
                language_code=language_code,
                stability=stability,
                similarity_boost=similarity_boost,
                style=style,
                use_speaker_boost=use_speaker_boost,
                speed=speed,
                advanced_voice_settings=advanced_voice_settings,
            )

        try:
            order = self.create_order(template_id=template_id, input_text=text)
        except PaygTopupRequired as exc:
            if not confirm_payg_topup:
                raise
            order = self.create_order(
                template_id=template_id,
                input_text=text,
                confirm_payg_topup=True,
                quote_token=exc.quote_token,
            )

        order = self.wait_for_order(
            order["id"], poll_interval=poll_interval, timeout=timeout
        )

        if order["status"] == "partially_completed":
            self.retry_failed_items(order["id"])
            order = self.wait_for_order(
                order["id"], poll_interval=poll_interval, timeout=timeout
            )

        if order["status"] not in ("completed", "result_delivered"):
            raise LumeanAPIError(
                0,
                f"Order {order['id']} finished with status "
                f"'{order['status']}' instead of completed",
                order,
            )

        result = order.get("result") or {}
        files = result.get("files") or []
        if not files:
            raise LumeanAPIError(0, f"Order {order['id']} completed with no output files", order)

        audio_path = self.download_file(files[0], out_path)

        subtitle_paths: list[Path] = []
        if download_subtitles:
            out_path = Path(out_path)
            for service_path in result.get("service_files") or []:
                ext = Path(service_path).suffix
                sub_out = out_path.with_suffix(ext)
                subtitle_paths.append(self.download_file(service_path, sub_out))

        return {
            "order_id": order["id"],
            "status": order["status"],
            "audio_path": audio_path,
            "subtitle_paths": subtitle_paths,
        }
