# Quality

## What was judged, and how

Each mesh is rendered and a panel is built comparing it against a fiber-weave
reference at the same scale, with joint normalisation
(`painel_fibras.py --win 1024 --passo 256`). The judgement is visual and
comparative: does the unknown look like the reference?

Criterion, fixed in mid-August and unchanged since:

- Fiber at 8.6-9.4 µm is a **wide band**, 70-150 px, not a thin streak.
- What confirms a single sheet is the **weave**: a checker pattern, bands
  crossing in two directions.
- **approve** — coherent weave over most of the panel.
- **partial** — at least one continuous patch of weave, several cm², with the
  rest melting.
- **reject** — no region follows the weave.
- A hole does not reject. Melting does.

Partial counts as usable because the prize asks for 10 letters inside a single
4 cm² area, and a typical winding here is 2-14 cm². Half of a good winding is
still several times the minimum.

## Results

84 panels judged in two sittings on 31 August, sampled systematically across
scrolls and wraps.

53 usable (approve or partial), 31 reject — 63%.

Failure mode is uniform: every rejection is melting. No swirls, no lamination.
Three of the partials melt along a diagonal, which suggests a preferred
direction tied to the fit geometry rather than to the papyrus.

## The wrap effect

Crossing the first 40 verdicts against the winding number:

| wrap | usable | reject | rate |
|---|---|---|---|
| w020 | 10 | 2 | 83% |
| w040 | 2 | 2 | 50% |
| w060 | 2 | 2 | 50% |
| w080 | 3 | 5 | 38% |
| w100 | 4 | 8 | 33% |

Monotonic across all five levels. The mechanism is plausible: the further from
the umbilicus, the longer the winding and the more chance for the surface to
leave the sheet. An independent measurement in August on PHerc1218 found CT
coverage falling from 100% at w020 to 4% at w148.

**Confirmation.** 44 previously unjudged w020 panels were then judged: 27
approve, 5 partial, 12 reject — 73% usable, against a base rate of 55% across
all wraps. The prediction was 83% and the margin declared before judging was
70-95%. Confirmed, at the low end.

Within w020 the rate by scroll is PHerc0800 83%, PHerc0211 77%, PHerc0813 73%,
PHerc0125 62% — all above base, and the spread between scrolls is smaller than
the spread between wraps.

## A test that failed its own criterion

Before finding the wrap effect we tested whether the screening metrics predict
the eye. Component count separated with an AUC of 0.364 (usable vs reject),
and three related metrics agreed. That looked promising.

It went to a blind test: 20 unjudged panels, 10 from the low-count end and 10
from the high-count end, renamed and shuffled, key sealed. Result: 70% usable
in the low-count group against 30% in the high-count group. A 40-point gap,
but the criterion set in advance required 80% in the good group. **Inconclusive
by its own rule.**

Unsealing the key showed why: the low-count group was almost all w020 and the
high-count group almost all w080/w100. Component count was not measuring mesh
quality — it was measuring distance from the umbilicus. Outer windings have
more area, hence more components.

The wrap effect is the simpler explanation, and it is known before any
processing. That is why it is the one reported here.

## Limits

- 84 of 340 meshes judged. The rest carry no verdict.
- One judge, no blinding in the two main sittings (the blind protocol was used
  only for the metric test above).
- The criterion is a comparison against one reference panel. It is written
  down so it can be disputed.
- The panel header reads "PHerc1447" — an inherited hard-coded label, ignore it.
- Per-cell counts in the wrap table are small: 12 panels at w020, 4 at w040.
  The monotonicity across five levels is what carries the claim, not any single
  cell.
