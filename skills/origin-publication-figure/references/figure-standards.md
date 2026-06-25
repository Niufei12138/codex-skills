# Scientific Figure Standards

## Sizes

- Default to single-column figures when possible.
- Use 85 mm width for single-column targets and 180 mm width for double-column targets when a venue requires it.
- Prefer a flatter aspect ratio for ordinary XY plots.
- Use square/equal aspect only when X and Y represent the same quantity or a 1:1 relationship matters.

## Typography

- Keep text consistent across the full figure set.
- Origin default: Arial, because it is robust in exported Origin figures.
- Manuscript alternative: Times New Roman if requested by the user or venue.
- Do not put a plot title inside the figure unless the user specifically needs a standalone presentation graphic.
- Put context in the caption or final summary, not in a large in-figure title.

## Color

Use a colorblind-safe discrete order for category/series colors:

1. `#0072B2` blue
2. `#D55E00` vermillion
3. `#009E73` bluish green
4. `#E69F00` orange
5. `#CC79A7` reddish purple
6. `#56B4E9` sky blue
7. `#F0E442` yellow
8. `#000000` black

For more than eight categories, ask the user whether to merge categories, split panels, or add line/symbol encodings. Do not invent a long set of saturated colors.

For continuous color, prefer perceptually ordered maps such as Viridis or Cividis. Avoid Jet, Rainbow, HSV rainbows, and other non-uniform maps unless the user explicitly overrides.

## Plot Types

- Scatter: use for independent observations or calibration points.
- Line or line+symbol: use for ordered sweeps, time series, spectra, kinetics, and dose-response curves.
- Bar/column: use only for categorical aggregates; include uncertainty or raw points when possible.
- Box/violin/histogram: use for distributions instead of hiding distribution shape behind bars.
- Dual Y axis: use sparingly, only when two quantities share X but have genuinely different units/scales. Match left-axis labels/ticks/series color and right-axis labels/ticks/series color. Avoid internal labels unless there is clear empty space.
- Heatmaps/contours: include a labeled color scale and a clear Z quantity with units.

## Fitting

- Fit only when the model is scientifically meaningful.
- Use data symbols plus a visually distinct fit curve in the final figure. Keep detailed Origin fit reports in the source project or final summary, not as large embedded tables inside the plot area.
- Remove or avoid auto-generated confidence/prediction bands when they obscure the data or dominate the figure; include them only when uncertainty visualization is part of the requested result.
- Report model, parameters, uncertainty/statistics returned by Origin, and any obvious caveat.
- Do not imply causality or model validity from a styled fit alone.

## Export

- Save `.opju` for editability.
- Prefer vector export (`svg` or `pdf`) for manuscript graphics.
- Also export a raster preview (`png`) or submission raster (`tiff`) when requested.
- Verify file existence and size after export.
