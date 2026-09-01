# Surface meshes for eight prize-eligible scrolls

340 tifxyz surface meshes covering eight of the thirteen scrolls eligible for
the First Letters prize. 1,935 cm² of surface in total.

**340 produced, 84 inspected by eye.** None were discarded: the index says
which ones were looked at and what the verdict was.

They were fitted on the 9 µm scans (8.64 µm for PHerc0800 and PHerc0268), using
the Vesuvius Challenge team's own tools: the spiral fitter and
`vc_render_tifxyz` from villa, run over a grid of z windows. 

Looking through the open data bucket on 1 September 2026, I found published
surfaces for only one of the thirteen eligible scrolls (PHerc1447, four
segments). I may well have missed some. If that reading is roughly right, there
is a gap here, and this is an attempt to fill part of it.

This is meant as a stopgap. Several projects in the community are working on
automated meshing at a scale and speed this cannot match, and when one of them
reaches the eligible scrolls the gap should close properly. Until then, these
are surfaces that can be rendered today.

## What is here

| scroll | meshes | inspected |
|---|---|---|
| PHerc0125 | 62 | 12 |
| PHerc0211 | 90 | 25 |
| PHerc0257 | 6 | 0 |
| PHerc0268 | 6 | 0 |
| PHerc0358 | 3 | 0 |
| PHerc0800 | 95 | 23 |
| PHerc0813 | 75 | 24 |
| PHerc0826 | 3 | 0 |

Each mesh is one winding of one fit window: `x.tif`, `y.tif`, `z.tif` and
`meta.json`, grid scale 0.05, about 128 KB each. That is the same scale the
team publishes its own PHerc0139 meshes at.

`data/index.csv` lists every mesh with its area, the physical-veto metrics
from our screening run (component counts and line pitch, forward and reverse,
dark and light polarity), and the eye verdict where one exists.

## How to use them

**Render a surface volume.** The meshes are plain tifxyz, so `vc_render_tifxyz`
takes them directly:

```
vc_render_tifxyz \
  --remote-url https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/PHerc0800/volumes/20250521135224-8.640um-1.2m-116keV-masked.zarr \
  --segmentation meshes/PHerc0800/z14672_w020 \
  --group-idx 0 --scale 1 --num-slices 31 --slice-step 1 --cache-gb 16 \
  --zarr-output out.zarr
```

**Open one in VC3D.** It wants a project, so `volpkg_template/` has the
structure ready. Copy a mesh into `paths/`, then:

1. `File → Open Project...`, pick the folder; VC3D offers to convert it to
   `.volpkg.json`, accept.
2. `File → Attach Remote Zarr...` with the scroll's volume URL.
3. In the Volume Package panel, pick the volume in the `Volume` dropdown and
   the mesh in the surface list.

We tested this end to end: the mesh renders with CT texture and the orthogonal
views track it. Details in `docs/USAGE.md`.

## Quality

84 of the 340 were inspected against a fiber-weave reference; 63% of those show usable weave over most or
part of the panel, and 37% melt.

Quality depends strongly on how far the winding sits from the umbilicus:

| wrap | usable | rate |
|---|---|---|
| w020 | 10/12 | 83% |
| w040 | 2/4 | 50% |
| w060 | 2/4 | 50% |
| w080 | 3/8 | 38% |
| w100 | 4/12 | 33% |

A second, larger sample of 44 previously unjudged w020 panels came out at 73%
usable, against a 55% base rate across all wraps. So the effect replicates,
though not at the 83% of the first sample.

There is a trade-off here, and it is worth stating plainly. Area grows with
the winding number, almost linearly: about 2.2 cm² at w020, 4.3 at w040, 6.3 at
w060, 8.1 at w080, 10.0 at w100. So the windings that hold up best are also the
smallest ones. The prize asks for 10 letters inside a single 4 cm² area, and a
w020 mesh is roughly half that. A w100 mesh is more than twice it, but two out
of three melt.

Practical reading: for a single mesh with enough area in one piece, the middle
wraps are the compromise. For reliable surface to accumulate across many
windows, w020 is the better yield. `index.csv` has both numbers per mesh so you
can pick.

If you only want the better ones, filter `index.csv` on `wrap = w020`. The
whole reasoning, including a blind test that failed its own criterion, is in
`docs/QUALITY.md`.

## How they were made

The team's spiral fitter in its minimal configuration: umbilicus plus lasagna,
no patches, no winding constraints. This is the route available for eligible scrolls
that have no annotation pack. Then flatten, then one mesh per winding, then
`vc_render_tifxyz`.

All of it is villa code, unmodified. `docs/METHOD.md` has the window geometry
and the settings used, for anyone who wants to run the same route elsewhere.

## Limits

- 256 of the 340 have no eye verdict.
- Eight scrolls, not thirteen. The remaining five had no validated minimal-route
  geometry when this was assembled.
- The verdict is one person's visual judgement against a reference panel, not a
  measurement. The criterion is written down so you can disagree with it.
- Meshes are one winding each, not grown segments. They are small.

## AI assistance

Produced with LLM assistance, directed and reviewed by me against real
scroll data. Every number here comes from a file in this repository.

## License

MIT.
