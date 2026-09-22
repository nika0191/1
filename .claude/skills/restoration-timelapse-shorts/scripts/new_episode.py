#!/usr/bin/env python3
"""Create an episode folder with a production plan and ready-to-paste prompts.

Usage:
  python3 new_episode.py --slug water-tower --object "1912 brick water tower" \
      --place "Vyborg, Russia" --twist "restored as it was" [--stages 6] [--kind building|vehicle|decay]
"""
import argparse
import pathlib
import textwrap

CAMERA_LOCK = (
    "Vertical 9:16, locked-off tripod camera, eye level from 30 m away, 35mm lens, "
    "same framing in every image, overcast soft daylight, photorealistic, documentary photo, "
    "no text, no watermark."
)

EDIT_PREFIX = (
    "Edit this exact image. Keep the camera, framing, perspective, lighting, background and the "
    "object's geometry EXACTLY the same. Change only the following:"
)

STAGES = {
    "building": [
        ("Clearing", "debris and weeds removed, the ground is cleared and leveled, a small excavator and a dumpster on site, 3 workers in orange vests"),
        ("Scaffolding & demolition", "scaffolding covers the facade, damaged roof removed down to the beams, protective green mesh, stacks of new bricks and timber"),
        ("Structure", "new roof structure and rafters installed, walls repaired with fresh brick patches, new window frames without glass"),
        ("Envelope closed", "new roof covering finished, windows glazed, scaffolding half removed, facade plastered but unpainted"),
        ("Finishing", "scaffolding removed, facade painted, decorative details restored, landscaping started, fresh gravel path"),
        ("Final", "fully restored and alive, blue hour light, warm lights glowing in the windows, lush garden, a few people walking in"),
    ],
    "vehicle": [
        ("Clearing", "vegetation and soil around it removed, a tow truck and a small crane on site, 3 workers in overalls"),
        ("Lifting", "the vehicle is lifted on jacks and a crane, rotten parts removed and stacked neatly"),
        ("Rust removal", "sandblasted to bare metal, patches of new steel welded in, sparks"),
        ("Primer", "fully covered in grey primer, new glass installed, wheels refurbished"),
        ("Paint & chrome", "glossy original factory paint, polished chrome, restored lettering and emblems"),
        ("Final", "fully restored, headlights on, blue hour, ready to move, light steam or exhaust, reflections on wet ground"),
    ],
    "decay": [
        ("First cracks", "fine cracks in the walls, faded paint, a few weeds at the base"),
        ("Peeling", "paint peeling in large patches, a couple of broken windows, rust streaks"),
        ("Overgrown", "vines climbing the facade, most windows broken, roof sagging"),
        ("Collapse", "roof partially collapsed, trees growing inside, debris everywhere"),
        ("Ruin", "only the shell remains, thick vegetation, moss, total abandonment"),
        ("Rebirth teaser", "the same ruin at dawn with the first scaffolding pole standing in front, a single worker looking at it"),
    ],
}

DEFAULT_INTRIGUE = {
    "building": "a birch tree growing through the roof",
    "vehicle": "it is sunk to its wheels in the forest soil with young trees growing around it",
    "decay": "a family is walking out of the brand-new building on its opening day",
}

VIDEO_TMPL = (
    "Construction timelapse. Locked-off static camera, no camera movement. Workers move fast in "
    "time-lapse, clouds race across the sky, shadows sweep across the ground. {action}. Realistic "
    "physics, continuous transformation from the first frame to the last. Audio: construction "
    "ambience - hammering, drills, angle grinder, distant voices, birds. No music."
)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--object", required=True, help='e.g. "1912 brick water tower on a hill"')
    p.add_argument("--place", default="", help='e.g. "Vyborg, Russia"')
    p.add_argument("--years", default="40")
    p.add_argument("--intrigue", default="", help="one striking detail in the first frame")
    p.add_argument("--twist", default="restored as it was")
    p.add_argument("--kind", choices=sorted(STAGES), default="building")
    p.add_argument("--stages", type=int, default=6)
    p.add_argument("--root", default="episodes")
    a = p.parse_args()

    if not a.intrigue:
        a.intrigue = DEFAULT_INTRIGUE[a.kind]

    ep = pathlib.Path(a.root) / a.slug
    for sub in ("frames", "clips", "audio", "out"):
        (ep / sub).mkdir(parents=True, exist_ok=True)

    stages = STAGES[a.kind][: max(2, min(a.stages, len(STAGES[a.kind])))]
    where = f" in {a.place}" if a.place else ""

    anchor = (
        f"{CAMERA_LOCK}\nAn abandoned {a.object}{where}, left to decay for {a.years} years. "
        f"{a.intrigue[0].upper() + a.intrigue[1:]}. Broken windows, rust streaks, moss, overgrown weeds, "
        "piles of debris. Melancholic mood, realistic textures, high detail."
    )

    lines = [
        f"# Episode: {a.slug}",
        "",
        f"- **Object:** {a.object}",
        f"- **Place:** {a.place or '-'}",
        f"- **Twist:** {a.twist}",
        f"- **Kind:** {a.kind}",
        "",
        "## Frames (save as frames/00.png, 01.png, ...)",
        "",
        "### 00 - Anchor (text-to-image)",
        "```",
        anchor,
        "```",
    ]
    for i, (name, change) in enumerate(stages, 1):
        lines += [
            "",
            f"### {i:02d} - {name} (edit frame {i-1:02d})",
            "```",
            f"{EDIT_PREFIX}\n{change}.",
            "```",
        ]

    lines += ["", "## Clips (save as clips/01.mp4, 02.mp4, ...)", ""]
    for i, (name, change) in enumerate(stages, 1):
        lines += [
            f"### Clip {i:02d}: frame {i-1:02d} -> frame {i:02d} ({name})",
            "Flow -> Frames to Video, 9:16, start = previous frame, end = this frame.",
            "```",
            VIDEO_TMPL.format(action=change[0].upper() + change[1:]),
            "```",
            "",
        ]

    lines += [
        "## Assembly",
        "```bash",
        f"bash .claude/skills/restoration-timelapse-shorts/scripts/assemble.sh {ep} --speed 1.25 --hook \"Left to rot for {a.years} years\"",
        "```",
        "",
        "## Metadata (draft - refine before upload)",
        f"- Title: This Abandoned {a.object.split(' on ')[0].title()} Comes Back to Life [AI concept]",
        "- Description: 2 lines of the object's real story + question: \"What should we restore next?\"",
        "- Hashtags: #constructiontimelapse #beforeandafter #restoration #abandoned",
        "- Studio: enable \"Altered or synthetic content\"",
        "",
        "## Checklist",
        "- [ ] Anchor frame has one clear intrigue detail",
        "- [ ] Geometry identical across all frames (windows, horizon, trees)",
        "- [ ] Each clip starts on the previous clip's last frame",
        "- [ ] First 1.5 s = most dramatic ruin + hook text",
        "- [ ] Final shot is a 'wow' and loops into the first frame",
        "- [ ] Duration 20-35 s, loudness normalized",
        "- [ ] AI disclosure ticked on upload",
    ]

    (ep / "plan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(textwrap.dedent(f"""\
        Created {ep}/
          plan.md  - prompts for {len(stages)} stages + clips + metadata
          frames/ clips/ audio/ out/"""))


if __name__ == "__main__":
    main()
