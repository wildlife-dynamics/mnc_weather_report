"""
Generate the MNC Weather Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mnc_weather_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mnc_weather_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Weather Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MNC Weather Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Daily weather summaries and time-series charts from GMMF weather stations", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mnc_weather_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>mnc_weather_report</b> workflow retrieves weather station "
      "observations from the EarthRanger subject group <b>ER2ER - From GMMF</b>, "
      "extracts seven meteorological variables from each observation's JSON "
      "detail field, computes daily aggregates per weather station, and "
      "renders an interactive time-series line chart for each variable."),
    sp(4),
    p("The workflow delivers:"),
    bullet("1 daily weather summary CSV — all seven variables aggregated per station and date"),
    bullet("7 line charts (HTML + PNG) — one per meteorological variable, "
           "coloured by weather station"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output", "Type", "Description"],
            ["weather_summary_table.csv",
             "CSV", "Daily per-station summary: sum precipitation, mean temperature/wind/humidity/pressure, max gusts"],
            ["precipitation_readings_over_time",
             "HTML / PNG", "Daily total precipitation (mm) per weather station"],
            ["temperature_readings_over_time",
             "HTML / PNG", "Daily mean surface air temperature (°C) per weather station"],
            ["wind_speed_readings_over_time",
             "HTML / PNG", "Daily mean wind speed per weather station"],
            ["wind_gusts_readings_over_time",
             "HTML / PNG", "Daily maximum wind gusts per weather station"],
            ["soil_temperature_readings_over_time",
             "HTML / PNG", "Daily mean soil temperature (°C) per weather station"],
            ["relative_humidity_readings_over_time",
             "HTML / PNG", "Daily mean relative humidity per weather station"],
            ["atmospheric_pressure_readings_over_time",
             "HTML / PNG", "Daily mean atmospheric pressure per weather station"],
        ],
        [5.5*cm, 2*cm, W - 7.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",        "0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.43.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.8.*",   "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connection"),
    make_table(
        [
            ["Connection", "Task", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch weather station observations from the subject group "
             "'ER2ER - From GMMF'"],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    note("This workflow does not require Google Earth Engine or any "
         "Dropbox file downloads."),
    sp(6),
    h2("2.3  Subject group (fixed)"),
    p("The subject group name is hardcoded in the spec as "
      "<b>'ER2ER - From GMMF'</b> and is not user-configurable. "
      "All observations are fetched with filter: clean, "
      "raise_on_empty: false, include_details: false, "
      "include_subjectsource_details: false."),
    sp(6),
    h2("2.4  Grouper"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: []). "
      "Data is not split by any grouping dimension. The grouper is "
      "passed through to the temporal index and dashboard only."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. OBSERVATION INGESTION AND VARIABLE EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Observation Ingestion and Variable Extraction"),
    hr(),
    p("Weather observations are fetched as subject group observations and "
      "then processed through a sequential extraction chain. Each step "
      "reads from the <b>extra__observation_details</b> JSON field and "
      "appends one new float column."),
    sp(6),
    h2("3.1  Observation retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",                       "get_subjectgroup_observations"],
            ["subject_group_name",         "'ER2ER - From GMMF' (hardcoded)"],
            ["filter",                     "clean"],
            ["raise_on_empty",             "false"],
            ["include_details",            "false"],
            ["include_subjectsource_details","false"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("3.2  Sequential variable extraction"),
    p("Task: <b>extract_value_from_json_column</b> — applied seven times in "
      "a chain, each reading from <b>extra__observation_details</b> and "
      "writing a new float column. Each step receives the output of the "
      "previous step as its input DataFrame:"),
    make_table(
        [
            ["Step", "field_name_options", "output_column_name", "output_type"],
            ["1", "precipitation",        "precipitation",        "float"],
            ["2", "surface_air_temperature","temperature",        "float"],
            ["3", "wind_speed",           "wind_speed",           "float"],
            ["4", "wind_gusts",           "wind_gusts",           "float"],
            ["5", "soil_temperature",     "soil_temperature",     "float"],
            ["6", "relative_humidity",    "relative_humidity",    "float"],
            ["7", "atmospheric_pressure", "atmospheric_pressure", "float"],
        ],
        [1*cm, 5*cm, 4.5*cm, W - 10.5*cm],
    ),
    note("field_name_options is a list, allowing the extractor to try "
         "multiple possible key names in the JSON. Only the first matching "
         "key found in each record is used."),
    sp(6),
    h2("3.3  Date extraction and column renaming"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "extract_column_as_type",
             "Extract <b>fixtime</b> as output_type: <b>date</b> into a "
             "new column <b>date</b>. This strips the time component for "
             "daily grouping in the summary table."],
            ["2", "map_columns",
             "Rename <b>extra__subject__name → weather_station</b> "
             "(raise_if_not_found: true). This column identifies which "
             "physical weather station produced each observation."],
            ["3", "add_temporal_index",
             "Add temporal index using time_col: <b>fixtime</b>, "
             "groupers: [], cast_to_datetime: true, format: mixed."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. DAILY WEATHER SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Daily Weather Summary"),
    hr(),
    p("Task: <b>summarize_df</b>. Observations are aggregated to daily "
      "resolution per weather station using the following aggregation "
      "rules (reset_index: true):"),
    make_table(
        [
            ["Variable", "Aggregation", "Rationale"],
            ["precipitation",       "sum",  "Total daily rainfall accumulation"],
            ["temperature",         "mean", "Average surface air temperature for the day"],
            ["wind_speed",          "mean", "Average wind speed for the day"],
            ["wind_gusts",          "max",  "Peak gust recorded during the day"],
            ["soil_temperature",    "mean", "Average soil temperature for the day"],
            ["relative_humidity",   "mean", "Average relative humidity for the day"],
            ["atmospheric_pressure","mean", "Average atmospheric pressure for the day"],
        ],
        [4*cm, 2.5*cm, W - 6.5*cm],
    ),
    sp(4),
    p("The summary DataFrame is grouped by <b>[weather_station, date]</b> "
      "producing one row per station per day. It is persisted to disk as "
      "<b>weather_summary_table.csv</b> and reused as the input for all "
      "seven line charts."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. LINE CHARTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Line Charts"),
    hr(),
    p("Seven line charts are generated from the daily weather summary, "
      "one per meteorological variable. All use <b>draw_line_chart</b> "
      "with identical layout parameters, differing only in the y-axis "
      "column and label."),
    sp(6),
    h2("5.1  Shared chart configuration"),
    make_table(
        [
            ["Parameter", "Value"],
            ["smoothing",          "null"],
            ["x_column",           "date"],
            ["category_column",    "weather_station"],
            ["line_kwargs shape",  "linear"],
            ["title",              "null (no title displayed)"],
            ["showlegend",         "true"],
            ["fontsize",           "20"],
            ["fontcolor",          "#2c3e50"],
            ["plot_bgcolor",       "#f5f5f5 (light grey background)"],
            ["xaxis title",        "Date"],
            ["xaxis tickformat",   "%Y-%m-%d"],
            ["xaxis tickangle",    "-45°"],
            ["xaxis rangemode",    "auto"],
            ["yaxis tickformat",   ".1f (1 decimal place)"],
            ["legend_title",       "Weather Station"],
            ["hovermode",          "x unified"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("The precipitation chart additionally sets showgrid: true, "
         "gridcolor: '#e0e0e0', gridwidth: 1 on the x-axis, making the "
         "grid lines visible for easier reading of daily totals."),
    sp(6),
    h2("5.2  Per-chart y-axis and output filename"),
    make_table(
        [
            ["Chart", "y_column", "y-axis title", "Output filename"],
            ["Precipitation",
             "precipitation",
             "Precipitation (mm)",
             "precipitation_readings_over_time.html"],
            ["Temperature",
             "temperature",
             "Average Temperature (°C)",
             "temperature_readings_over_time.html"],
            ["Wind speed",
             "wind_speed",
             "Average wind speed",
             "wind_speed_readings_over_time.html"],
            ["Wind gusts",
             "wind_gusts",
             "Max wind gusts",
             "wind_gusts_readings_over_time.html"],
            ["Soil temperature",
             "soil_temperature",
             "Average Temperature (°C)",
             "soil_temperature_readings_over_time.html"],
            ["Relative humidity",
             "relative_humidity",
             "Average humidity",
             "relative_humidity_readings_over_time.html"],
            ["Atmospheric pressure",
             "atmospheric_pressure",
             "Average pressure",
             "atmospheric_pressure_readings_over_time.html"],
        ],
        [3.5*cm, 3.5*cm, 4*cm, W - 11*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. PNG CONVERSION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. PNG Conversion"),
    hr(),
    p("All seven chart HTML files are converted to PNG in a single "
      "<b>html_to_png</b> call, with all paths passed as a list:"),
    make_table(
        [
            ["Parameter", "Value"],
            ["html_path",            "List of all 7 chart HTML paths"],
            ["width",                "1 280 px"],
            ["height",               "720 px"],
            ["full_page",            "false"],
            ["device_scale_factor",  "2.0 (effective resolution: 2 560 × 1 440)"],
            ["wait_for_timeout",     "10 ms (static Plotly HTML — no tile maps)"],
            ["timeout",              "0 (no overall page timeout)"],
            ["max_concurrent_pages", "5 (up to 5 charts rendered in parallel)"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("Batching all seven charts into one html_to_png call with "
         "max_concurrent_pages: 5 is more efficient than seven separate "
         "calls. The 10 ms wait_for_timeout is sufficient because all "
         "charts are static Plotly HTML with no external tile dependencies."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    make_table(
        [
            ["File", "Description"],
            ["weather_summary_table.csv",
             "Daily per-station summary table with all 7 aggregated weather variables"],
            ["precipitation_readings_over_time.html / .png",
             "Daily total precipitation (mm) line chart per weather station"],
            ["temperature_readings_over_time.html / .png",
             "Daily mean surface air temperature (°C) line chart"],
            ["wind_speed_readings_over_time.html / .png",
             "Daily mean wind speed line chart"],
            ["wind_gusts_readings_over_time.html / .png",
             "Daily maximum wind gusts line chart"],
            ["soil_temperature_readings_over_time.html / .png",
             "Daily mean soil temperature (°C) line chart"],
            ["relative_humidity_readings_over_time.html / .png",
             "Daily mean relative humidity line chart"],
            ["atmospheric_pressure_readings_over_time.html / .png",
             "Daily mean atmospheric pressure line chart"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Workflow Execution Logic"),
    hr(),
    h2("8.1  Per-task skip conditions"),
    p("This workflow does not use a global <b>task-instance-defaults</b> block. "
      "Every task from observation retrieval onwards carries its own explicit "
      "skipif block:"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",        "Skip this task if any input DataFrame is empty"],
            ["any_dependency_skipped", "Skip this task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("8.2  Linear pipeline"),
    p("The entire workflow is a single linear chain with no branching, "
      "mapvalues fan-out, or parallel processing of data. The seven "
      "variable extraction steps are strictly sequential — each step "
      "receives the enriched DataFrame from the previous step. "
      "The seven chart generation steps are logically independent but "
      "all read from the same shared <b>daily_weather</b> summary DataFrame."),
    sp(6),
    h2("8.3  No maps or spatial outputs"),
    p("This workflow produces no EcoMaps, scatter layers, or spatial "
      "visualisations — only tabular CSV data and time-series line charts. "
      "There are no draw_map, create_scatterplot_layer, or "
      "zoom_map_and_screenshot calls."),
    sp(6),
    h2("8.4  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b> which packages "
      "workflow details, time range, and groupers. The <b>widgets</b> list "
      "is empty — no single-value or map widgets are configured."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-workflows-core",        "0.22.18.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.43.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.8.*"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
