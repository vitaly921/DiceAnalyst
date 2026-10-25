from pathlib import Path

GRAPH_IMAGES_DIR = Path(__file__).resolve().parent / "images" / "graphs"

CHARTS_TYPES = (
    "bar_horizontal",
    "bar_vertical",
    "circle",
    "CDF",
    "convergence",
    "heat_map",
    "boxplot_horizontal",
    "boxplot_vertical",
    "linear",
    "scatter",
    "stacked"
)

CHART_PREVIEW_IMAGES = {
    "bar_horizontal": GRAPH_IMAGES_DIR / "bar_hor.jpg",
    "bar_vertical": GRAPH_IMAGES_DIR / "bar_vert.jpg",
    "circle": GRAPH_IMAGES_DIR / "circle.jpg",
    "CDF": GRAPH_IMAGES_DIR / "CDF.jpg",
    "convergence": GRAPH_IMAGES_DIR / "convergence.jpg",
    "heat_map": GRAPH_IMAGES_DIR / "heat_map.jpg",
    "boxplot_horizontal": GRAPH_IMAGES_DIR / "hor_boxplot.jpg",
    "boxplot_vertical": GRAPH_IMAGES_DIR / "vert_boxplot.jpg",
    "linear": GRAPH_IMAGES_DIR / "linear.jpg",
    "scatter": GRAPH_IMAGES_DIR / "scater.jpg",
    "stacked": GRAPH_IMAGES_DIR / "stacked.jpg",
}