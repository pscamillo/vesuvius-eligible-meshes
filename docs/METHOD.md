# Method

## The route

Minimal spiral fit: umbilicus and lasagna only, no patches, no winding
constraints. This is the route Paul Henderson's 18 August post presents as the
first step, and the only one available for eligible scrolls that have no
annotation pack.

The code handles this case explicitly (`losses.py:573-575`): with an empty
patch list, the umbilicus and shell anchors still apply and the patch
radius/DT terms become inert zeros. Active constraints are the umbilicus
(`loss_weight_umbilicus` 1.25) and dense normals (`loss_weight_dense_normals`
1e2, `dense_spacing` 12).

Chain: pick a z window -> download that window's lasagna -> fit -> flatten ->
one mesh per winding -> render -> ink inference -> physical vetoes.

## Three corrections to the published material

All three were verified in the code and against the bucket.

**1. `lasagna_scale` is 4, not 2.** Groups 0 and 1 do not exist in the bucket;
the published level is 2, at 1/4 of the volume. Measured on PHerc1218
(23247/5812) and PHerc0125 (20840/5210). With 2, the fit raises a RuntimeError
about an empty z-ROI.

**2. The flag is `disable_patches`, not `input_disable_patches`.**
`fit_spiral.py:206` defines `disable_patches`; `input_disable_patches` does not
exist in the code. Passing the wrong name leaves patches enabled and the fit
looks for supervision that is not there.

**3. Tracks are required.** Without `tracks_<scroll>/`, the fit returns
`winding range [0, 0)` — no windings. With them, it returns a real range. This
was the root cause of early failures on PHerc0125.

## Window geometry

Each window is the umbilicus median plus an offset, ±400 slices — 800 voxels,
about 7.5 mm of height — aligned to 16. Offsets are drawn without replacement
from a grid of multiples of 600 up to ±6000.

Success markers for a fit: `winding range [0, N)` with N > 0, step 0 with
dense normals and a non-zero umbilicus, exit 0. About 10 minutes on an
RTX 5070.

Some windows never fit. PHerc0211 below z2512 and PHerc0800 above z17664 are
known limits, marked and skipped.

## Render

`vc_render_tifxyz --group-idx 0 --scale 1 --num-slices 31 --slice-step 1
--cache-gb 16`, with the volume cache cleared before every winding. The cache
carried over between windings caused a failure on PHerc0800 whose cause we
never isolated ("nothing found at path ''"); clearing per winding fixed it and
costs little.

## Ink screening (not part of this package, but it produced the metrics)

Inference with the published 9 µm checkpoint `hybrid_3d2d-seed43/step-060000`,
band 7-24 of the 31 slices, `--direction both`. Then physical vetoes at
threshold 0.60 (0.30 saturates at about 92% of the valid area), minimum
component area 300 px, and a valid mask eroded by 40 px — that erosion kills
the strip-edge artifact, which was the first false-positive mode we catalogued.

Both polarities are screened, dark and light. Ink polarity is not fixed: it
is a property of the scan and reconstruction pair, not of the ink chemistry.
On PHerc Paris 4 about 65-71% of ink reads brighter than its surroundings;
PHerc0139 is neutral; PHerc0814 reads dark.

The component counts and pitch values in `data/index.csv` come from this step,
for both directions and both polarities.

## Area

`area_vx2` in each mesh's `meta.json` is in squared voxels. Converted with
8.64 µm for PHerc0800 and PHerc0268, 9.362 µm for the rest.

VC3D shows `-1.000` in its area column for these meshes — it reads a different
field. The number is in the metadata and in `index.csv`.
