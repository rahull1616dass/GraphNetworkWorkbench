import type { VisualizationSpec } from "vega-embed";

export default {
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "description": "A node-link diagram with force-directed layout, depicting character co-occurrence in the novel Les Misérables.",
  "width": 700,
  "height": 500,
  "padding": 0,
  "autosize": "none",
  "signals": [
    { "name": "cx", "update": "width / 2" },
    { "name": "cy", "update": "height / 2" },
    { "name": "nodeRadius", "value": 10, "bind": { "input": "range", "min": 1, "max": 50, "step": 1 } },
    { "name": "nodeCharge", "value": -30, "bind": { "input": "range", "min": -100, "max": 10, "step": 1 } },
    { "name": "linkDistance", "value": 15, "bind": { "input": "range", "min": 5, "max": 100, "step": 1 } },
    { "name": "gravityX", "value": 0.1, "bind": { "input": "range", "min": 0, "max": 1 } },
    { "name": "gravityY", "value": 0.1, "bind": { "input": "range", "min": 0, "max": 1 } },
    { "name": "static", "value": true, "bind": { "input": "checkbox" } },
    { "name": "fix", "value": false, "on": [
        { "events": "symbol:mouseout[!event.buttons], window:mouseup", "update": "false" },
        { "events": "symbol:mouseover", "update": "fix || true" },
        { "events": "[symbol:mousedown, window:mouseup] > window:mousemove!", "update": "xy()", "force": true }
      ] },
    { "name": "node", "value": null, "on": [
        { "events": "symbol:mouseover", "update": "fix === true ? item() : node" }
      ] },
    { "name": "restart", "value": false, "on": [{ "events": { "signal": "fix" }, "update": "fix && fix.length" }] }
  ],
  "data": [
    { "name": "node-data" },
    { "name": "link-data" }
  ],
  "scales": [
    { "name": "colorNodes", "type": "ordinal", "domain": { "data": "node-data", "field": "group" }, "range": { "scheme": "category10" } },
    { "name": "edgeColor", "type": "ordinal", "domain": { "data": "link-data", "field": "result" }, "range": { "scheme": "category10" } }
  ],
  "marks": [
    {
      "name": "edges",
      "type": "path",
      "from": { "data": "link-data" },
      "interactive": true,
      "encode": {
        "update": {
          "stroke": { "scale": "edgeColor", "field": "result" },
          "strokeWidth": { "value": 3 }
        }
      },
      "transform": [
        {
          "type": "linkpath",
          "require": { "signal": "force" },
          "shape": "line",
          "sourceX": "datum.source.x",
          "sourceY": "datum.source.y",
          "targetX": "datum.target.x",
          "targetY": "datum.target.y"
        }
      ]
    },
    {
      "name": "nodes",
      "type": "symbol",
      "zindex": 1,
      "from": { "data": "node-data" },
      "on": [
        {
          "trigger": "fix",
          "modify": "node",
          "values": "fix === true ? {fx: node.x, fy: node.y} : {fx: fix[0], fy: fix[1]}"
        },
        { "trigger": "!fix", "modify": "node", "values": "{fx: null, fy: null}" }
      ],
      "encode": {
        "enter": {
          "fill": { "scale": "colorNodes", "field": "group" },
          // "stroke": { "value": "white" },
          "xfocus": { "signal": "cx" },
          "yfocus": { "signal": "cy" }
        },
        "update": {
          "size": { "signal": "2 * nodeRadius * nodeRadius" },
          "cursor": { "value": "pointer" }
        }
      },
      "transform": [
        {
          "type": "force",
          "iterations": 100,
          "restart": { "signal": "restart" },
          "static": { "signal": "static" },
          "signal": "force",
          "forces": [
            { "force": "center", "x": { "signal": "cx" }, "y": { "signal": "cy" } },
            { "force": "x", "x": "xfocus", "strength": { "signal": "gravityX" } },
            { "force": "y", "y": "yfocus", "strength": { "signal": "gravityY" } },
            { "force": "collide", "radius": { "signal": "linkDistance" } },
            { "force": "nbody", "strength": { "signal": "nodeCharge" } },
            { "force": "link", "links": "link-data", "distance": { "signal": "linkDistance" } }
          ]
        }
      ]
    }
  ]
} as VisualizationSpec;
