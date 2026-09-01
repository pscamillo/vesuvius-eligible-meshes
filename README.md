# Surface meshes for eight prize-eligible scrolls

340 tifxyz surface meshes from the minimal spiral-fit route, covering eight of
the thirteen scrolls eligible for the First Letters prize. 1,935 cm² of
surface in total. 84 of them have been inspected by eye and carry a quality
verdict.

As of 1 September 2026, twelve of the thirteen eligible scrolls have no
published surface at all in the open data bucket. Only PHerc1447 does, with
four segments. This is an attempt to close part of that gap.

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

**Render a surface volume** — the meshes are plain tifxyz, so `vc_render_tifxyz`
takes them directly:

```
vc_render_tifxyz \
  --remote-url https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/PHerc0800/volumes/20250521135224-8.640um-1.2m-116keV-masked.zarr \
  --segmentation meshes/PHerc0800/z14672_w020 \
  --group-idx 0 --scale 1 --num-slices 31 --slice-step 1 --cache-gb 16 \
  --zarr-output out.zarr
```

**Open one in VC3D** — VC3D wants a project, so `volpkg_template/` has the
structure ready. Copy a mesh into `paths/`, then:

1. `File → Open Project...`, pick the folder; VC3D offers to convert it to
   `.volpkg.json`, accept.
2. `File → Attach Remote Zarr...` with the scroll's volume URL.
3. In the Volume Package panel, pick the volume in the `Volume` dropdown and
   the mesh in the surface list.

We tested this end to end: the mesh renders with CT texture and the orthogonal
views track it. Details in `docs/USAGE.md`.

## Quality

The meshes were produced automatically and are not curated. 84 were inspected
against a fiber-weave reference; 63% of those show usable weave over most or
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

Minimal spiral fit: umbilicus plus lasagna, no patches, no winding
constraints — the route available for eligible scrolls with no annotation
pack. Then flatten, then one mesh per winding.

The recipe corrects three things that the published material gets wrong for
this route. They are written down in `docs/METHOD.md`, with the reason for
each.

## Limits

- Not curated. 256 of the 340 have no eye verdict.
- Eight scrolls, not thirteen. The remaining five had no validated minimal-route
  geometry when this was assembled.
- The verdict is one person's visual judgement against a reference panel, not a
  measurement. The criterion is written down so you can disagree with it.
- Meshes are one winding each, not grown segments. They are small.

## AI assistance

The pipeline scripts, the analysis and the first draft of this text were
produced with heavy LLM assistance, directed and reviewed by me against real
scroll data. Every number here comes from a file in this repository.

## License

MIT.
