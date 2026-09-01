# Usage

## Rendering a surface volume

The meshes are plain tifxyz. `vc_render_tifxyz` from VC3D takes them with no
conversion:

```
vc_render_tifxyz \
  --remote-url <scroll volume URL> \
  --segmentation meshes/PHerc0800/z14672_w020 \
  --group-idx 0 --scale 1 \
  --num-slices 31 --slice-step 1 --cache-gb 16 \
  --zarr-output out.zarr
```

Volume URLs, by scroll:

| scroll | volume |
|---|---|
| PHerc0125 | `20250821151825-9.362um-1.2m-113keV-masked.zarr` |
| PHerc0211 | `20250821151803-9.362um-1.2m-113keV-masked.zarr` |
| PHerc0257 | `20250821151750-9.362um-1.2m-113keV-masked.zarr` |
| PHerc0268 | `20251110183117-8.640um-1.2m-116keV-masked.zarr` |
| PHerc0358 | `20250821151737-9.362um-1.2m-113keV-masked.zarr` |
| PHerc0800 | `20250521135224-8.640um-1.2m-116keV-masked.zarr` |
| PHerc0813 | `20250821151723-9.362um-1.2m-113keV-masked.zarr` |
| PHerc0826 | `20250821151701-9.362um-1.2m-113keV-masked.zarr` |

Prefix: `https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/<scroll>/volumes/`

Clear the volume cache between windings. A cache carried over caused a render
failure on PHerc0800 that we never isolated; clearing per winding fixed it.

## Opening one in VC3D

VC3D opens projects, not loose meshes. `volpkg_template/` has the structure:

```
volpkg_template/
  config.json          {"name": ..., "version": 1}
  volumes/
  paths/               put the mesh directory here
```

1. Copy a mesh into `paths/`, e.g.
   `paths/0800_z14672_w020/{x,y,z}.tif` plus `meta.json`.
2. `File -> Open Project...` and select `volpkg_template`. VC3D will say it
   needs converting to `.volpkg.json`, accept, and pick where to save it.
3. `File -> Attach Remote Zarr...` and paste the scroll's volume URL.
4. In the Volume Package panel, select the volume in the `Volume` dropdown.
   The mesh appears in the surface list; click it.

The Surface view then renders the winding with CT texture, and the XY and YZ
views show where it sits inside the scroll.

Two things to expect. The area column reads `-1.000`, VC3D looks for a field
we do not write; the area is in `data/index.csv`. And the first render pulls
chunks over the network, so it takes a moment.

## Reading the index

`data/index.csv`, one row per mesh:

- `scroll`, `window_z`, `wrap`, identity
- `area_cm2`, from `area_vx2` in the mesh metadata
- `n_comp_fwd`, `n_comp_rev`, component counts from the ink screening run,
  forward and reverse inference
- `pitch_*_dark`, `pitch_*_light`, line-pitch p-value per direction and
  polarity
- `gate_verdict`, `aprova`, `parcial`, `reprova`, or empty if not judged
- `path`, where it came from

The screening metrics are included because they are what we had; they are not
a quality score. A blind test showed component count tracks the winding number,
not mesh quality, see `QUALITY.md`.
