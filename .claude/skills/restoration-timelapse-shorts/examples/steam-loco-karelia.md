# Episode: steam-loco-karelia

- **Object:** Soviet steam locomotive with a black boiler and red wheels, abandoned on a forgotten railway siding
- **Place:** a Karelian pine forest
- **Twist:** restored and steams off again
- **Kind:** vehicle

## Frames (save as frames/00.png, 01.png, ...)

### 00 - Anchor (text-to-image)
```
Vertical 9:16, locked-off tripod camera, eye level from 30 m away, 35mm lens, same framing in every image, overcast soft daylight, photorealistic, documentary photo, no text, no watermark.
An abandoned Soviet steam locomotive with a black boiler and red wheels, abandoned on a forgotten railway siding in a Karelian pine forest, left to decay for 50 years. It is sunk to its wheels in the forest soil with young trees growing around it. Broken windows, rust streaks, moss, overgrown weeds, piles of debris. Melancholic mood, realistic textures, high detail.
```

### 01 - Clearing (edit frame 00)
```
Edit this exact image. Keep the camera, framing, perspective, lighting, background and the object's geometry EXACTLY the same. Change only the following:
vegetation and soil around it removed, a tow truck and a small crane on site, 3 workers in overalls.
```

### 02 - Lifting (edit frame 01)
```
Edit this exact image. Keep the camera, framing, perspective, lighting, background and the object's geometry EXACTLY the same. Change only the following:
the vehicle is lifted on jacks and a crane, rotten parts removed and stacked neatly.
```

### 03 - Rust removal (edit frame 02)
```
Edit this exact image. Keep the camera, framing, perspective, lighting, background and the object's geometry EXACTLY the same. Change only the following:
sandblasted to bare metal, patches of new steel welded in, sparks.
```

### 04 - Primer (edit frame 03)
```
Edit this exact image. Keep the camera, framing, perspective, lighting, background and the object's geometry EXACTLY the same. Change only the following:
fully covered in grey primer, new glass installed, wheels refurbished.
```

### 05 - Paint & chrome (edit frame 04)
```
Edit this exact image. Keep the camera, framing, perspective, lighting, background and the object's geometry EXACTLY the same. Change only the following:
glossy original factory paint, polished chrome, restored lettering and emblems.
```

### 06 - Final (edit frame 05)
```
Edit this exact image. Keep the camera, framing, perspective, lighting, background and the object's geometry EXACTLY the same. Change only the following:
fully restored, headlights on, blue hour, ready to move, light steam or exhaust, reflections on wet ground.
```

## Clips (save as clips/01.mp4, 02.mp4, ...)

### Clip 01: frame 00 -> frame 01 (Clearing)
Flow -> Frames to Video, 9:16, start = previous frame, end = this frame.
```
Construction timelapse. Locked-off static camera, no camera movement. Workers move fast in time-lapse, clouds race across the sky, shadows sweep across the ground. Vegetation and soil around it removed, a tow truck and a small crane on site, 3 workers in overalls. Realistic physics, continuous transformation from the first frame to the last. Audio: construction ambience - hammering, drills, angle grinder, distant voices, birds. No music.
```

### Clip 02: frame 01 -> frame 02 (Lifting)
Flow -> Frames to Video, 9:16, start = previous frame, end = this frame.
```
Construction timelapse. Locked-off static camera, no camera movement. Workers move fast in time-lapse, clouds race across the sky, shadows sweep across the ground. The vehicle is lifted on jacks and a crane, rotten parts removed and stacked neatly. Realistic physics, continuous transformation from the first frame to the last. Audio: construction ambience - hammering, drills, angle grinder, distant voices, birds. No music.
```

### Clip 03: frame 02 -> frame 03 (Rust removal)
Flow -> Frames to Video, 9:16, start = previous frame, end = this frame.
```
Construction timelapse. Locked-off static camera, no camera movement. Workers move fast in time-lapse, clouds race across the sky, shadows sweep across the ground. Sandblasted to bare metal, patches of new steel welded in, sparks. Realistic physics, continuous transformation from the first frame to the last. Audio: construction ambience - hammering, drills, angle grinder, distant voices, birds. No music.
```

### Clip 04: frame 03 -> frame 04 (Primer)
Flow -> Frames to Video, 9:16, start = previous frame, end = this frame.
```
Construction timelapse. Locked-off static camera, no camera movement. Workers move fast in time-lapse, clouds race across the sky, shadows sweep across the ground. Fully covered in grey primer, new glass installed, wheels refurbished. Realistic physics, continuous transformation from the first frame to the last. Audio: construction ambience - hammering, drills, angle grinder, distant voices, birds. No music.
```

### Clip 05: frame 04 -> frame 05 (Paint & chrome)
Flow -> Frames to Video, 9:16, start = previous frame, end = this frame.
```
Construction timelapse. Locked-off static camera, no camera movement. Workers move fast in time-lapse, clouds race across the sky, shadows sweep across the ground. Glossy original factory paint, polished chrome, restored lettering and emblems. Realistic physics, continuous transformation from the first frame to the last. Audio: construction ambience - hammering, drills, angle grinder, distant voices, birds. No music.
```

### Clip 06: frame 05 -> frame 06 (Final)
Flow -> Frames to Video, 9:16, start = previous frame, end = this frame.
```
Construction timelapse. Locked-off static camera, no camera movement. Workers move fast in time-lapse, clouds race across the sky, shadows sweep across the ground. Fully restored, headlights on, blue hour, ready to move, light steam or exhaust, reflections on wet ground. Realistic physics, continuous transformation from the first frame to the last. Audio: construction ambience - hammering, drills, angle grinder, distant voices, birds. No music.
```

## Assembly
```bash
bash .claude/skills/restoration-timelapse-shorts/scripts/assemble.sh episodes/steam-loco-karelia --speed 1.25 --hook "Left to rot for 50 years"
```

## Metadata (draft - refine before upload)
- Title: This Abandoned Soviet Steam Locomotive With A Black Boiler And Red Wheels, Abandoned Comes Back to Life [AI concept]
- Description: 2 lines of the object's real story + question: "What should we restore next?"
- Hashtags: #constructiontimelapse #beforeandafter #restoration #abandoned
- Studio: enable "Altered or synthetic content"

## Checklist
- [ ] Anchor frame has one clear intrigue detail
- [ ] Geometry identical across all frames (windows, horizon, trees)
- [ ] Each clip starts on the previous clip's last frame
- [ ] First 1.5 s = most dramatic ruin + hook text
- [ ] Final shot is a 'wow' and loops into the first frame
- [ ] Duration 20-35 s, loudness normalized
- [ ] AI disclosure ticked on upload

## Final package (steam-loco-karelia)

**Hook (0-1.5 s):** "Паровоз 50 лет в лесу" / EN: "50 years lost in the forest"

**Titles (pick one, A/B test via "Test & compare"):**
- RU: `Паровоз 50 лет гнил в карельском лесу… 😳 [ИИ-концепт]`
- EN: `Abandoned Soviet Steam Train Found in the Forest → Fully Restored`
- EN alt: `This Train Was Lost in the Forest for 50 Years [AI concept]`
- DE: `Verlassene Dampflok im Wald – komplett restauriert [KI-Konzept]`

**Description (RU):**
Этот паровоз полвека простоял на забытом разъезде в карельской тайге — сквозь кабину проросла берёза.
Что было бы, если его восстановить? Концепт-таймлапс, созданный с помощью ИИ.
Что восстановить следующим: вагон-ресторан, трамвай или водонапорную башню? Пиши в комментариях 👇
#constructiontimelapse #beforeandafter #restoration #steamtrain #abandoned

**Pinned comment:** "Голосуем за следующий объект: 1️⃣ вагон-ресторан 2️⃣ трамвай 1950-х 3️⃣ водонапорная башня"

**Structure (target 28 s):**
| t | clip | content |
|---|---|---|
| 0-1.5 | 00 still/zoom | birch in the cab, hook text |
| 1.5-6 | 01 | clearing: trees cut, soil dug out |
| 6-11 | 02 | crane lift, jacks |
| 11-16 | 03 | sandblasting + welding sparks (ASMR) |
| 16-21 | 04 | primer → black paint + red wheels |
| 21-28 | 05 | final: headlight on, steam, whistle, starts moving |

## Generated frames (BFL FLUX.2 request ids, 22.09.2026)
| # | Stage | request_id |
|---|---|---|
| 00 | Anchor (seed 4217) | 3dda0e87-4a04-496c-a281-2bed32bd76e0 |
| 00b | Anchor alt (seed 9931) | c5cb2829-6533-4840-886f-f85629f6dc85 |
| 01 | Clearing | 84e81ed7-a0e4-4fd3-848b-c937dff4cf27 |
| 02 | Jacks + sandblast + welding | 84ddf9af-8cbd-48c9-9654-41c5449473ae |
| 03 | Primer | 93fb0a20-053d-43ad-be44-27ef2516fb16 |
| 04 | Painted | 677038fb-8074-425a-8ef6-57c59c933f6d |
| 05 | Final blue hour + steam | df315600-b93c-4d97-84b3-cae945e8a2a0 |

All stages are edits of the anchor (parallel), so the camera is shared. Signed URLs expire in 24 h —
download from app.bfl.ai history into frames/ for Flow.

## Video (BFL FLUX.3)
- Draft storyboard, 6 keyframes (00-05), 20 s, 9:16, audio: `f9c06e11-9dcb-43ea-b093-51b9236e0813`
- Next: if the draft is good -> `enhance_video` (fhd); if a stage drifts -> redo that pair in Google Flow
  (Frames to Video) and assemble with assemble.sh.
