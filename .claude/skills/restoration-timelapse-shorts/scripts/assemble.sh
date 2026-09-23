#!/usr/bin/env bash
# Assemble restoration timelapse clips into a YouTube Short (1080x1920, 30 fps, H.264/AAC, -14 LUFS).
#
# Usage:
#   assemble.sh <episode_dir> [--speed 1.25] [--music file.mp3] [--music-vol 0.35]
#               [--hook "text"] [--hook-sec 1.8] [--font /path/font.ttf] [--out name.mp4]
#
# Takes <episode_dir>/clips/*.mp4 (and .mov/.webm) in name order. Writes <episode_dir>/out/.
# Set FFMPEG=/path/to/ffmpeg to use a specific binary.
set -euo pipefail

FF="${FFMPEG:-ffmpeg}"
EP=""; SPEED="1.0"; MUSIC=""; MUSIC_VOL="0.35"; HOOK=""; HOOK_SEC="1.8"; FONT=""; OUT="final.mp4"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --speed) SPEED="$2"; shift 2;;
    --music) MUSIC="$2"; shift 2;;
    --music-vol) MUSIC_VOL="$2"; shift 2;;
    --hook) HOOK="$2"; shift 2;;
    --hook-sec) HOOK_SEC="$2"; shift 2;;
    --font) FONT="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    -h|--help) sed -n '2,10p' "$0"; exit 0;;
    *) EP="$1"; shift;;
  esac
done

[[ -n "$EP" && -d "$EP/clips" ]] || { echo "Usage: $0 <episode_dir> [options] (needs <episode_dir>/clips/)" >&2; exit 1; }
command -v "$FF" >/dev/null || { echo "ffmpeg not found (set FFMPEG=...)" >&2; exit 1; }
awk -v s="$SPEED" 'BEGIN{exit !(s>=0.5 && s<=2.0)}' || { echo "--speed must be between 0.5 and 2.0" >&2; exit 1; }

shopt -s nullglob
CLIPS=("$EP"/clips/*.mp4 "$EP"/clips/*.mov "$EP"/clips/*.webm)
shopt -u nullglob
[[ ${#CLIPS[@]} -gt 0 ]] || { echo "No clips in $EP/clips" >&2; exit 1; }
IFS=$'\n' CLIPS=($(printf '%s\n' "${CLIPS[@]}" | sort)); unset IFS

mkdir -p "$EP/out"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,setpts=PTS/${SPEED},fps=30"
AF="aresample=48000,aformat=channel_layouts=stereo,atempo=${SPEED}"

echo "Normalizing ${#CLIPS[@]} clip(s) at speed x${SPEED}..."
: > "$TMP/list.txt"
i=0
for c in "${CLIPS[@]}"; do
  i=$((i+1)); n="$TMP/$(printf '%03d' "$i").mp4"
  info="$("$FF" -hide_banner -i "$c" 2>&1 || true)"
  if [[ "$info" == *"Audio:"* ]]; then
    "$FF" -hide_banner -loglevel error -y -i "$c" -vf "$VF" -af "$AF" \
      -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 "$n"
  else
    "$FF" -hide_banner -loglevel error -y -i "$c" -f lavfi -i anullsrc=r=48000:cl=stereo \
      -vf "$VF" -map 0:v -map 1:a -shortest \
      -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 "$n"
  fi
  echo "file '$n'" >> "$TMP/list.txt"
  echo "  [$i] $(basename "$c")"
done

"$FF" -hide_banner -loglevel error -y -f concat -safe 0 -i "$TMP/list.txt" -c copy "$TMP/joined.mp4"

# Hook text overlay (read from file so quotes/Cyrillic need no escaping)
VPOST="null"
FILTERS="$("$FF" -hide_banner -filters 2>/dev/null || true)"
if [[ -n "$HOOK" && "$FILTERS" != *" drawtext "* ]]; then
  echo "WARNING: this ffmpeg has no drawtext filter (built without freetype) - hook text skipped." >&2
  echo "         Install a full ffmpeg build or add the hook in CapCut/YouTube editor." >&2
  HOOK=""
fi
if [[ -n "$HOOK" ]]; then
  if [[ -z "$FONT" ]]; then
    for f in /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf \
             /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf \
             "/System/Library/Fonts/Supplemental/Arial Bold.ttf" \
             /Library/Fonts/Arial\ Bold.ttf \
             C:/Windows/Fonts/arialbd.ttf; do
      [[ -f "$f" ]] && { FONT="$f"; break; }
    done
  fi
  [[ -n "$FONT" ]] || { echo "No font found for --hook; pass --font" >&2; exit 1; }
  printf '%s' "$HOOK" > "$TMP/hook.txt"
  cp "$FONT" "$TMP/font.ttf"
  VPOST="drawtext=fontfile=$TMP/font.ttf:textfile=$TMP/hook.txt:fontsize=78:fontcolor=white:borderw=6:bordercolor=black@0.85:x=(w-text_w)/2:y=h*0.18:enable='lt(t,${HOOK_SEC})'"
fi

if [[ -n "$MUSIC" ]]; then
  [[ -f "$MUSIC" ]] || { echo "Music file not found: $MUSIC" >&2; exit 1; }
  FC="[0:v]${VPOST}[v];[1:a]volume=${MUSIC_VOL},aresample=48000[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
  "$FF" -hide_banner -loglevel error -y -i "$TMP/joined.mp4" -stream_loop -1 -i "$MUSIC" \
    -filter_complex "$FC" -map "[v]" -map "[a]" -shortest \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -r 30 -movflags +faststart "$EP/out/$OUT"
else
  "$FF" -hide_banner -loglevel error -y -i "$TMP/joined.mp4" \
    -vf "$VPOST" -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -r 30 -movflags +faststart "$EP/out/$OUT"
fi

# Frames for loop / hook review
"$FF" -hide_banner -loglevel error -y -i "$EP/out/$OUT" -frames:v 1 -q:v 2 "$EP/out/first.jpg"
"$FF" -hide_banner -loglevel error -y -sseof -0.1 -i "$EP/out/$OUT" -frames:v 1 -q:v 2 -update 1 "$EP/out/last.jpg"

DUR="$({ "$FF" -hide_banner -i "$EP/out/$OUT" 2>&1 || true; } | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | head -1)"
echo "Done: $EP/out/$OUT (duration $DUR). Review first.jpg / last.jpg for hook and loop."
awk -v d="$DUR" 'BEGIN{split(d,t,":"); s=t[1]*3600+t[2]*60+t[3]; if (s>60) print "WARNING: longer than 60 s - trim for Shorts best practice"; else if (s<15) print "NOTE: under 15 s - consider adding a stage or final orbit"}'
