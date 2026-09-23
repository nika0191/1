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

# Each stage is (name, image_change, video_action).
# image_change: what the STILL frame shows. Deliberately has NO people/vehicles in it - a still
# that has a worker in it gets edited forward stage by stage, so that worker's exact pose gets
# copied unchanged into every later frame ("frozen worker" bug). Keep stills clean; only describe
# the physical state of the object.
# video_action: what happens in the TRANSITION clip between this still and the next one. This is
# where people and machinery belong, and each stage's action should be visibly different work -
# don't reuse the same pose/description across stages.
STAGES = {
    "building": [
        (
            "Clearing",
            "all overgrown vegetation, vines and debris are removed from the walls and ground, "
            "the ground is cleared and leveled, the path is swept clean; the building itself is "
            "still damaged and unpainted, no scaffolding yet, no people or tools in the shot",
            "Workers arrive, strip the ivy and vines off the walls by hand, rake fallen leaves and "
            "debris into a pile, and haul it away in a wheelbarrow",
        ),
        (
            "Scaffolding & demolition",
            "wooden scaffolding covers the facade, the damaged roof sections are removed down to "
            "the bare beams, a few stacks of new bricks and timber sit neatly to one side, the "
            "ground stays clean, no people or tools in the shot",
            "A crew erects wooden scaffolding around the building, climbs it, and pulls off the "
            "last damaged roof beams, tossing debris down to a dumpster below",
        ),
        (
            "Structure",
            "new roof structure and rafters are installed, walls are repaired with fresh brick or "
            "timber patches, new window frames are in place but without glass yet, no people or "
            "tools in the shot",
            "Workers on the scaffolding hammer new rafters into place while others below lay fresh "
            "bricks and set new window frames into the wall openings",
        ),
        (
            "Envelope closed",
            "the new roof covering is finished, all windows are glazed with clear glass, the "
            "scaffolding is mostly gone, the facade is plastered but still unpainted, no people or "
            "tools in the shot",
            "A crew nails the final roof shingles into place, fits clear glass into each window "
            "frame, and begins taking the scaffolding down section by section",
        ),
        (
            "Finishing",
            "the facade is freshly painted, decorative details are restored, landscaping has begun "
            "with a fresh gravel path, no people or tools in the shot",
            "One worker rolls fresh paint across the facade in broad strokes while another lays a "
            "gravel path and plants shrubs along it",
        ),
        (
            "Final",
            "fully restored and alive, blue hour light, warm lights glowing in every window, a lush "
            "garden, no people in the shot",
            "As dusk falls the crew packs up their tools and leaves; warm light switches on in each "
            "window one by one and the garden looks lush and cared for",
        ),
    ],
    "vehicle": [
        (
            "Clearing",
            "the vegetation and soil around it are removed, the ground beneath and around it is "
            "cleared and leveled, no tow truck, crane, people or tools in the shot",
            "A crew arrives with a tow truck and a small crane, clears the vegetation and soil "
            "around the vehicle by hand, and rigs lifting straps to it",
        ),
        (
            "Lifting",
            "the vehicle is lifted slightly on jacks, rotten or rusted parts have been removed and "
            "stacked neatly to one side, no crane, people or tools in the shot",
            "Workers operate a small crane and hydraulic jacks to lift the vehicle, then unbolt and "
            "remove the rotten parts, stacking them neatly on a tarp",
        ),
        (
            "Rust removal",
            "sandblasted down to bare metal, a few patches of new welded steel are visible, no "
            "people or tools in the shot",
            "A worker in a mask sandblasts the body down to bare metal while another welds in fresh "
            "steel patches, sparks flying",
        ),
        (
            "Primer",
            "fully covered in even grey primer, new glass is installed, the wheels are refurbished, "
            "no people or tools in the shot",
            "Workers spray an even coat of grey primer over the bare metal, fit new glass, and "
            "refurbish the wheels one at a time",
        ),
        (
            "Paint & chrome",
            "glossy original factory paint, polished chrome trim, restored lettering and emblems, "
            "no people or tools in the shot",
            "A painter applies glossy factory-color paint in smooth passes while another polishes "
            "the chrome trim and reattaches the restored emblems",
        ),
        (
            "Final",
            "fully restored, headlights on, blue hour light, ready to move, a light haze of steam "
            "or exhaust, reflections on wet ground, no people in the shot",
            "As dusk falls the crew steps back and admires their work, then the headlights switch "
            "on and a light steam rises as the engine turns over for the first time",
        ),
    ],
    "decay": [
        (
            "First cracks",
            "fine cracks appear in the walls, the paint is starting to fade, a few weeds sprout at "
            "the base, no people in the shot",
            "Time passes quickly - no visible workers, just weather and neglect: rain streaks the "
            "walls and the first weeds take root at the base",
        ),
        (
            "Peeling",
            "paint peels in large patches, a couple of windows are broken, rust streaks appear, no "
            "people in the shot",
            "Wind and rain accelerate the decay - shutters bang loose, a window cracks and breaks, "
            "paint peels away in curling strips",
        ),
        (
            "Overgrown",
            "vines climb the facade, most windows are broken, the roofline is starting to sag, no "
            "people in the shot",
            "Vines creep up the walls month by month, more windows crack, and the roof begins to "
            "visibly sag under years of neglect",
        ),
        (
            "Collapse",
            "the roof is partially collapsed, trees are growing inside through the gaps, debris "
            "covers the ground, no people in the shot",
            "A section of the roof finally gives way, exposing the interior to the sky as young "
            "trees take root inside",
        ),
        (
            "Ruin",
            "only the shell remains, thick vegetation and moss cover every surface, total "
            "abandonment, no people in the shot",
            "The last walls settle into ruin, moss spreads across every surface, and the forest "
            "slowly reclaims the structure",
        ),
        (
            "Rebirth teaser",
            "the same ruin at dawn, the first scaffolding pole now stands in front of it, no people "
            "in the shot",
            "At dawn a truck arrives and a single worker steps out, looks up at the ruin, and sets "
            "down the first scaffolding pole",
        ),
    ],
}

DEFAULT_INTRIGUE = {
    "building": "a birch tree growing through the roof",
    "vehicle": "it is sunk to its wheels in the forest soil with young trees growing around it",
    "decay": "a family is walking out of the brand-new building on its opening day",
}

VIDEO_TMPL = (
    "Time-lapse, static locked-off camera, absolutely no camera movement. {action}. Clouds move "
    "fast across the sky, shadows sweep the ground, realistic physics, continuous transformation "
    "from the first frame to the last. Photorealistic. Audio: real construction sounds matching "
    "the action - hammering, sawing, footsteps, tools, no music."
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
        "piles of debris. Melancholic mood, realistic textures, high detail. No people in the shot."
    )

    lines = [
        f"# Episode: {a.slug}",
        "",
        f"- **Object:** {a.object}",
        f"- **Place:** {a.place or '-'}",
        f"- **Twist:** {a.twist}",
        f"- **Kind:** {a.kind}",
        "",
        "**Rule:** the still frames below never contain people, vehicles or tools - only the "
        "object's physical state. If a still has a worker in it, editing it forward copies that "
        "exact pose into every later frame (the \"frozen worker\" bug). People only appear inside "
        "the transition clips, each doing different, stage-appropriate work.",
        "",
        "## Frames (save as frames/00.png, 01.png, ...)",
        "",
        "### 00 - Anchor (text-to-image)",
        "```",
        anchor,
        "```",
    ]
    for i, (name, image_change, _video_action) in enumerate(stages, 1):
        lines += [
            "",
            f"### {i:02d} - {name} (edit frame {i-1:02d})",
            "```",
            f"{EDIT_PREFIX}\n{image_change}.",
            "```",
        ]

    lines += ["", "## Clips (save as clips/01.mp4, 02.mp4, ...)", ""]
    for i, (name, _image_change, video_action) in enumerate(stages, 1):
        lines += [
            f"### Clip {i:02d}: frame {i-1:02d} -> frame {i:02d} ({name})",
            "Flow -> Frames to Video, 9:16, start = previous frame, end = this frame. (Grok: "
            "start image = previous frame only, no end-frame lock.)",
            "```",
            VIDEO_TMPL.format(action=video_action[0].upper() + video_action[1:]),
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
        "- [ ] Anchor frame has one clear intrigue detail, no people",
        "- [ ] Geometry identical across all frames (windows, horizon, trees)",
        "- [ ] No still frame has a person/vehicle baked into it",
        "- [ ] Each transition clip's crew does different, visibly distinct work",
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
