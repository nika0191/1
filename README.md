# 1

Python-клиент и CLI для генерации озвучки через публичный API [Lumean](https://lumean.app)
(`https://api.lumean.app/api/public`).

## Установка

```bash
pip install -r requirements.txt
# или, чтобы получить команду `lumean` в PATH:
pip install -e .
```

## Ключ API

Ключ передаётся заголовком `X-API-KEY`. Не храните его в коде — используйте переменную окружения:

```bash
cp .env.example .env
# впишите в .env: LUMEAN_API_KEY=...
export $(grep -v '^#' .env | xargs)   # или используйте python-dotenv/direnv
```

Ключу нужны права `orders.write`, `orders.read`, `orders.download`, `templates.write`,
`templates.read`, `voices.read` (пресет `full`, либо `automation` + `templates.write`).

## CLI

Найти голос в библиотеке ElevenLabs:

```bash
lumean voices --search "male narrator" --language ru
```

Сгенерировать озвучку:

```bash
lumean generate --text "Привет! Это тестовая озвучка через Lumean API." \
  --voice-id <VOICE_ID> --language-code ru --out out.mp3
```

Дополнительно скачать субтитры (.srt/.vtt):

```bash
lumean generate --text-file script.txt --voice-id <VOICE_ID> --out out.mp3 --subtitles
```

Использовать уже существующий шаблон вместо auto-create:

```bash
lumean generate --text "..." --template-id <TEMPLATE_UUID> --out out.mp3
```

Посмотреть остаток лимитов:

```bash
lumean usage
```

Если квоты подписки не хватает, команда сообщит о необходимой доплате (PAYG) и `shortfall_lmc`.
Чтобы подтвердить автоматическую доплату из LMC-баланса, добавьте `--confirm-payg`.

## Как библиотека

```python
from lumean import LumeanClient

client = LumeanClient()  # берёт LUMEAN_API_KEY из окружения

result = client.synthesize_speech(
    text="Привет! Это тестовая озвучка через Lumean API.",
    voice_id="<VOICE_ID>",
    language_code="ru",
    out_path="out.mp3",
)
print(result["audio_path"], result["order_id"], result["status"])
```

`synthesize_speech` сам находит/создаёт TTS-шаблон под нужный `voice_id`, создаёт заказ,
дожидается его готовности (включая один автоматический `retry-failed`, если заказ пришёл
`partially_completed`) и скачивает готовый аудиофайл.

## Структура

- `lumean/client.py` — HTTP-клиент (`LumeanClient`) и обработка ошибок API.
- `lumean/cli.py` — команды `generate`, `voices`, `usage`.
