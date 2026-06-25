# OriginLab MCP Tool Map

This skill targets the installed `garethbeaumo/originlab-mcp` server exposed as `originlab`.

## Connection and Project

- Inspect connection: `get_origin_info`
- Release COM control: `release_origin`
- Reconnect: `reconnect_origin`
- Save source project: `save_project`
- Open existing source project: `open_project`
- Create new blank project only when requested: `new_project`
- Avoid `close_origin` unless the user explicitly asks to close Origin.

## Data

- CSV: `import_csv`
- Excel: `import_excel`
- Pasted/generated table text: `import_data_from_text`
- Inspect sheets: `list_worksheets`, `get_worksheet_info`, `get_worksheet_data`, `get_cell_value`
- Column roles and labels: `set_column_designations`, `set_column_labels`
- Derived columns: `set_column_formula`
- Sort/clear/delete only when explicitly useful: `sort_worksheet`, `clear_worksheet`, `delete_columns`

## Plotting

- Basic plot: `create_plot`
- Overlay data: `add_plot_to_graph`
- Double Y axis: `create_double_y_plot`
- Add layer: `add_graph_layer`
- Group series: `group_plots`
- Inspect graph: `list_graphs`, `get_graph_info`, `list_graph_templates`

## Style

- Baseline publication style: `apply_publication_style`
- Axis labels/ranges: `set_axis_title`, `set_axis_range`, `set_axis_step`, `set_axis_scale`
- Fonts and ticks: `set_graph_font`, `set_tick_style`
- Legend: `set_legend`
- Curves: `set_plot_color`, `set_plot_line_style`, `set_plot_line_width`, `set_plot_symbols`, `set_symbol_size`, `set_symbol_interior`, `set_plot_transparency`
- Error bars: `set_error_bar_style`
- Fill/colormap: `set_fill_area`, `set_plot_colormap`
- Annotations: `add_text_label`, `add_line_to_graph`, `set_graph_title`, `remove_graph_label`
- Legend cleanup: try `set_legend(visible=false)` first. If exported previews still show a default Origin legend, remove label objects with `remove_graph_label(label_name="Legend")` for the relevant layer.

## Fitting and Analysis

- Linear model: `linear_fit`
- Nonlinear model: `nonlinear_fit`
- Discover functions: `list_fit_functions`

## Export

- One graph: `export_graph`
- All graphs: `export_all_graphs`
- Worksheet CSV: `export_worksheet_to_csv`

## Escape Hatch

- `execute_labtalk` is high risk. Use it only when typed MCP tools cannot do the required operation.
- If typed tools cannot remove leftover Origin legends or labels, a narrow LabTalk cleanup is acceptable, for example hiding legends and removing known label names on the active graph. Keep commands short, activate the target graph/sheet first when needed, and verify state afterward with typed tools or exported previews.
