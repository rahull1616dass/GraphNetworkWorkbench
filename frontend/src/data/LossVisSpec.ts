import type { VisualizationSpec } from "vega-embed"

export default {

    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Loss function.",
    "mark": "line",
    "encoding": {
        "x": { "field": "epoch", "type": "quantitative" },
        "y": { "field": "loss", "type": "quantitative" }
    },
    "data": { "values": {} },
    "signals": []
} as VisualizationSpec
