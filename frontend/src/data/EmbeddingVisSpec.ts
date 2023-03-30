import type { VisualizationSpec } from "vega-embed";

export default {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "A scatterplot showing node embeddings.",
  "data": {
    "values": [] // This will be replaced with the actual data later
  },
  "mark": "point",
  "encoding": {
    "x": {
      "field": "x",
      "type": "quantitative",
      "scale": { "zero": false }
    },
    "y": {
      "field": "y",
      "type": "quantitative",
      "scale": { "zero": false }
    },
  }
} as VisualizationSpec;
