import type { VisualizationSpec } from "vega-embed";

export default {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "A scatterplot showing body mass and flipper lengths of penguins.",
        "data": {
          "url": "penguins.json"
        },
        "mark": "point",
        "encoding": {
          "x": {
            "field": "Flipper Length (mm)",
            "type": "quantitative",
            "scale": {"zero": false}
          },
          "y": {
            "field": "Body Mass (g)",
            "type": "quantitative",
            "scale": {"zero": false}
          },
          "color": {"field": "Species", "type": "nominal"},
          "shape": {"field": "Species", "type": "nominal"}
        }
           
} as VisualizationSpec;