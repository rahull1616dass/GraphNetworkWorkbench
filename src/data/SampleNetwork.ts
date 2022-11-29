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
        {
            "name": "nodeRadius",
            "value": 10,
            "bind": { "input": "range", "min": 1, "max": 50, "step": 1 }
        },
        {
            "name": "nodeCharge",
            "value": -30,
            "bind": { "input": "range", "min": -100, "max": 10, "step": 1 }
        },
        {
            "name": "linkDistance",
            "value": 15,
            "bind": { "input": "range", "min": 5, "max": 100, "step": 1 }
        },


        { "name": "gravityX", "value": 0.1, "bind": { "input": "range", "min": 0, "max": 1 } },
        { "name": "gravityY", "value": 0.1, "bind": { "input": "range", "min": 0, "max": 1 } },



        { "name": "static", "value": false, "bind": { "input": "checkbox" } },
        {
            "description": "State variable for active node fix status.",
            "name": "fix",
            "value": false,
            "on": [
                {
                    "events": "symbol:mouseout[!event.buttons], window:mouseup",
                    "update": "false"
                },
                { "events": "symbol:mouseover", "update": "fix || true" },
                {
                    "events": "[symbol:mousedown, window:mouseup] > window:mousemove!",
                    "update": "xy()",
                    "force": true
                }
            ]
        },
        {
            "description": "Graph node most recently interacted with.",
            "name": "node",
            "value": null,
            "on": [
                { "events": "symbol:mouseover", "update": "fix === true ? item() : node" }
            ]
        },
        {
            "description": "Flag to restart Force simulation upon data changes.",
            "name": "restart",
            "value": false,
            "on": [{ "events": { "signal": "fix" }, "update": "fix && fix.length" }]
        }
    ],
    "data": [
        {
            "name": "node-data"
        },
        {
            "name": "link-data"
        }
    ],
    "scales": [
        {
            "name": "color",
            "type": "ordinal",
            "domain": { "data": "node-data", "field": "group" },
            "range": { "scheme": "category20c" }
        }
    ],
    "marks": [
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
                    "fill": { "scale": "color", "field": "group" },
                    "stroke": { "value": "white" },

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
                    "iterations": 300,
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
        },
        {
            "type": "path",
            "from": { "data": "link-data" },
            "interactive": false,
            "encode": {
                "update": { "stroke": { "value": "#ccc" }, "strokeWidth": { "value": 0.5 } }
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
        }
    ]
} as VisualizationSpec