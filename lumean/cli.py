"""Command-line interface for Lumean text-to-speech generation."""

from __future__ import annotations

import argparse
import sys

from .client import (
    DEFAULT_BASE_URL,
    LumeanAPIError,
    LumeanClient,
    PaygTopupRequired,
    RateLimitExceeded,
    TokenQuotaExceeded,
)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-key", help="Lumean API key (default: $LUMEAN_API_KEY)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)


def cmd_generate(args: argparse.Namespace) -> int:
    if args.text_file:
        text = open(args.text_file, encoding="utf-8").read()
    else:
        text = args.text

    if not args.voice_id and not args.template_id:
        print("error: either --voice-id or --template-id is required", file=sys.stderr)
        return 2

    client = LumeanClient(api_key=args.api_key, base_url=args.base_url)

    try:
        result = client.synthesize_speech(
            text=text,
            out_path=args.out,
            voice_id=args.voice_id,
            template_id=args.template_id,
            model_id=args.model_id,
            language_code=args.language_code,
            stability=args.stability,
            similarity_boost=args.similarity_boost,
            style=args.style,
            use_speaker_boost=not args.no_speaker_boost,
            speed=args.speed,
            download_subtitles=args.subtitles,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
            confirm_payg_topup=args.confirm_payg,
        )
    except PaygTopupRequired as exc:
        print(
            "Subscription quota is not enough for this request.\n"
            f"  shortfall: {exc.shortfall_tokens} tokens "
            f"(~{exc.shortfall_lmc} LMC)\n"
            f"  quote valid until: {exc.expires_at}\n"
            "Re-run with --confirm-payg to pay the difference from your LMC balance.",
            file=sys.stderr,
        )
        return 3
    except TokenQuotaExceeded as exc:
        print(
            f"Token quota exceeded for window '{exc.window}' "
            f"({exc.used}/{exc.limit} used, {exc.requested} requested). "
            f"Resets at {exc.reset_at}.",
            file=sys.stderr,
        )
        return 4
    except RateLimitExceeded:
        print("Rate limit exceeded. Back off and retry later.", file=sys.stderr)
        return 4
    except LumeanAPIError as exc:
        print(f"Lumean API error: {exc}", file=sys.stderr)
        return 1

    print(f"order:  {result['order_id']} ({result['status']})")
    print(f"audio:  {result['audio_path']}")
    for path in result["subtitle_paths"]:
        print(f"subtitle: {path}")
    return 0


def cmd_voices(args: argparse.Namespace) -> int:
    client = LumeanClient(api_key=args.api_key, base_url=args.base_url)
    try:
        data = client.list_elevenlabs_voices(
            search=args.search,
            page=args.page,
            page_size=args.page_size,
            language_code=args.language,
            gender=args.gender,
        )
    except LumeanAPIError as exc:
        print(f"Lumean API error: {exc}", file=sys.stderr)
        return 1

    voices = data.get("voices", [])
    if not voices:
        print("No voices found.")
        return 0
    for v in voices:
        voice_id = v.get("voice_id", "?")
        name = v.get("name") or v.get("display_name") or "?"
        gender = v.get("gender", "?")
        lang = v.get("language") or v.get("locale") or "?"
        print(f"{voice_id}\t{name}\t{gender}\t{lang}")
    if data.get("has_more"):
        print(f"... more results on page {args.page + 1}", file=sys.stderr)
    return 0


def cmd_usage(args: argparse.Namespace) -> int:
    client = LumeanClient(api_key=args.api_key, base_url=args.base_url)
    try:
        usage = client.get_usage()
    except LumeanAPIError as exc:
        print(f"Lumean API error: {exc}", file=sys.stderr)
        return 1
    for entry in usage:
        print(
            f"{entry.get('service_code', '?'):<15} "
            f"{entry.get('limit_type', '?'):<10} "
            f"{entry.get('used')}/{entry.get('limit_value')} "
            f"(remaining: {entry.get('remaining')})"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lumean", description="Lumean TTS client")
    sub = parser.add_subparsers(dest="command", required=True)

    p_generate = sub.add_parser("generate", help="Generate speech from text")
    _add_common_args(p_generate)
    text_group = p_generate.add_mutually_exclusive_group(required=True)
    text_group.add_argument("--text", help="Text to synthesize")
    text_group.add_argument("--text-file", help="Path to a UTF-8 text file")
    p_generate.add_argument("--voice-id", help="ElevenLabs voice_id (see 'lumean voices')")
    p_generate.add_argument("--template-id", help="Existing Lumean template UUID")
    p_generate.add_argument("--model-id", default="eleven_multilingual_v2")
    p_generate.add_argument("--language-code", help="ISO-639-1 code, e.g. ru, en")
    p_generate.add_argument("--stability", type=float, default=0.5)
    p_generate.add_argument("--similarity-boost", type=float, default=0.75)
    p_generate.add_argument("--style", type=float, default=None)
    p_generate.add_argument("--speed", type=float, default=1.0)
    p_generate.add_argument("--no-speaker-boost", action="store_true")
    p_generate.add_argument("--out", default="speech.mp3")
    p_generate.add_argument("--subtitles", action="store_true", help="Also download .srt/.vtt")
    p_generate.add_argument("--poll-interval", type=float, default=2.0)
    p_generate.add_argument("--timeout", type=float, default=300.0)
    p_generate.add_argument(
        "--confirm-payg",
        action="store_true",
        help="Automatically pay the PAYG top-up if the subscription quota is insufficient",
    )
    p_generate.set_defaults(func=cmd_generate)

    p_voices = sub.add_parser("voices", help="Search the ElevenLabs voice library")
    _add_common_args(p_voices)
    p_voices.add_argument("--search")
    p_voices.add_argument("--language")
    p_voices.add_argument("--gender", choices=["male", "female"])
    p_voices.add_argument("--page", type=int, default=0)
    p_voices.add_argument("--page-size", type=int, default=30)
    p_voices.set_defaults(func=cmd_voices)

    p_usage = sub.add_parser("usage", help="Show current usage/limits")
    _add_common_args(p_usage)
    p_usage.set_defaults(func=cmd_usage)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
