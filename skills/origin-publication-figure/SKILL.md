---
name: origin-publication-figure
description: Create high-quality scientific and journal-ready figures in Origin/OriginPro using the local originlab MCP. Use when the user asks Codex to plot with Origin, make publication-quality or manuscript figures, polish scientific graphs, fit data for an Origin figure, export Origin figures, save .opju source files, or create reusable Origin figure outputs from CSV, Excel, pasted data, or existing Origin worksheets.
---

# Origin Publication Figure

Use the local `originlab` MCP as the tool layer and this skill as the figure-quality workflow. The default deliverable is an editable `.opju` source project plus high-quality exported figures.

## Core Workflow

1. Establish context:
   - Use `get_origin_info` first.
   - Inspect existing worksheets/graphs before creating duplicates when the user may already have data open.
   - Ask only for missing choices that materially change the figure: data source, X/Y/error/group mapping, figure type, fit model, output folder, target venue, or journal style.

2. Prepare data:
   - Use `import_csv`, `import_excel`, or `import_data_from_text`.
   - Set designations and labels when column roles are clear.
   - Preserve raw data; create derived columns with `set_column_formula` instead of overwriting measured columns.

3. Build the plot:
   - Use `create_plot` for ordinary XY plots, `add_plot_to_graph` for overlays, and `create_double_y_plot` only when units/scales genuinely require dual axes.
   - Use `linear_fit` or `nonlinear_fit` only when fitting answers the scientific question.
   - Keep fitting computation separate from final figure composition. Fit reports, result tables, confidence bands, and auto-generated legends may remain in the `.opju`, but do not leave them as final figure objects unless the user explicitly asks.
   - Show fit results with a clean fit curve, reference line, or concise annotation. If Origin adds crowded report tables, confidence/prediction bands, or cluttered legends to the graph, remove them or rebuild the final display from raw data plus a clean fit line.
   - Report fit parameters plainly. Do not hide weak fits behind styling.

4. Apply publication styling:
   - Start with `apply_publication_style`.
   - Fine-tune axes, legend, colors, line widths, symbols, error bars, and ranges with typed tools.
   - Default to no legend for one or two self-evident series. Use axis colors, direct labels, or a compact external legend only when needed for interpretation.
   - For double-Y plots, prefer left/right axis color and title matching over internal labels. Avoid placing text labels inside crowded data regions.
   - Prefer typed MCP tools over `execute_labtalk`; use LabTalk only as a last resort and explain why.

5. Export and save:
   - Always save the editable Origin project with `save_project` unless the user explicitly says not to.
   - Export at least one high-quality image. Prefer vector formats (`svg` or `pdf`) plus a raster preview (`png` or `tiff`) when supported.
   - Verify exported files exist and have non-trivial size.
   - Inspect exported raster previews when possible. If the preview shows overlapping text, clipped legends, report tables, misplaced annotations, empty plots, or cropped axes, fix the Origin graph and re-export before final response.
   - Use `release_origin` at the end so the user can operate Origin manually.

## Defaults

Use these defaults unless the user gives a target journal, template, or lab style:

- White background, no decorative effects, no chart title inside the figure.
- Axis titles include units, for example `Temperature (K)` or `Current density (mA cm^-2)`.
- Arial for Origin figures unless the user requests Times/serif. Keep typography consistent across axes, ticks, legends, and annotations.
- Axis title size about 24-28 pt; tick labels about 18-22 pt; legend about 18-20 pt.
- Inward ticks, minor ticks enabled, closed frame when appropriate, grid off unless it helps read the data.
- Main data lines about 1.5-2.5 pt; symbols size 7-10; error bars thinner than data lines with visible caps.
- Legends are optional, not automatic. Remove default Origin legends unless they add needed information; legends must not cover data, overlap the frame, or be clipped at export.
- Use colorblind-safe colors and distinct symbols. Do not use red/green as the only two encodings.
- Avoid rainbow/jet colormaps for quantitative data; use perceptually ordered maps such as Viridis/Cividis when available.

## Output Contract

For formal figure work, produce:

- `.opju` source project
- `svg` or `pdf` vector export when available
- `png` or `tiff` raster export for preview/submission workflows
- A short result summary: source file, graph name, fit results if any, exported paths, and any limitations

If an export format fails, keep the successful outputs and state the failed format clearly.

## Quality Gate

Before final response, check:

- Axis labels include units and are readable after export.
- Tick labels are not overcrowded.
- Lines, markers, and error bars remain visible at final size.
- Colors are distinguishable in colorblind and grayscale contexts.
- Legend/direct labels do not cover data.
- Axis ranges do not crop important values or outliers.
- Fit curves and statistics match the stated model.
- Origin-generated artifacts such as automatic legends, fit report tables, confidence bands, and prediction bands do not clutter the final figure.
- Exported files exist and are not empty.
- `.opju` source was saved unless explicitly skipped.

## References

Load these only when needed:

- `references/figure-standards.md`: detailed sizing, color, typography, and layout standards.
- `references/originlab-tool-map.md`: mapping from this workflow to the installed `garethbeaumo/originlab-mcp` tool names.
