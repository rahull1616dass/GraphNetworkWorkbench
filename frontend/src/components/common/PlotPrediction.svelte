<script lang="ts">
    import { selectedNetworkIndex, networksList } from "../../stores"
    import { default as vegaEmbed } from "vega-embed"
    import VisSpec from "../../data/VisSpec"
    import { updateVisSpec, setColorKey } from "../../util/visSpecUtil"
    import { onMount } from "svelte"
    import { Node, Link } from "../../definitions/network"
    import { HoverData } from "../../definitions/hoverData"
    import Hover from "../pages/Workbench/Plot/Hover.svelte"
    import { HoverType } from "../../definitions/hoverType"
    import cloneDeep from "lodash.clonedeep"
    import { PredictionResult } from "../../definitions/predictionResult"
    import type { Task } from "../../definitions/task"
    import type { Network } from "../../definitions/network"
    import { createEventDispatcher } from "svelte"

    const dispatch = createEventDispatcher()
    let hoverData: HoverData = undefined
    // Dynamically adjust the hover offset based on screen size
    const HOVER_OFFSET = {
      x: 100,
      y: 200,
    }
    export let currentNetwork: Network = undefined

    export let task: Task = undefined
    // Run an onMount function to initialize the plot
    onMount(() => { 
        loadNetwork()
    })
  
    function loadNetwork() {
      let networkToPlot: Network = cloneDeep(currentNetwork)
      networkToPlot.nodes.forEach((node) => {
        // If node.index is not in predictions, then that node was in the training set
        // @ts-ignore
        if (task.predictions[node.index] === undefined) {
          // @ts-ignore
          node.result = PredictionResult.IN_TRAIN_SET
        }
        // @ts-ignore
        else if(task.predictions[node.index] === node[task.yColumn].toString()) {
          // @ts-ignore
          node.result = PredictionResult.CORRECT
        }else {
          // @ts-ignore
          node.result = PredictionResult.WRONG
        }
      })
      

      updateVisSpec(networkToPlot, VisSpec)
      setColorKey(VisSpec, "result", ["#808080", "#FF0000", "#097969"]) // TODO: Change group to prediction
      vegaEmbed("#viz", VisSpec, { actions: false })
        .then((result) => {
          dispatch("predictionPlotLoaded", result.view)
          result.view.addEventListener("mouseover", function (event, item) {
            console.log("MOUSEOVER", item)
            if (item != undefined && item.datum != undefined) {
              // @ts-ignore
              if (item != undefined && item.path != undefined) {
                // @ts-ignore
                console.log(item.path)
                hoverData = new HoverData(
                  HoverType.LINK,
                  new Link(
                    item.datum.source.datum.name,
                    item.datum.target.datum.name,
                    item.datum.value
                  ),
                  undefined,
                  // @ts-ignore
                  event.clientX - HOVER_OFFSET.x,
                  // @ts-ignore
                  event.clientY - HOVER_OFFSET.y
                )
              } else {
                hoverData = new HoverData(
                  HoverType.NODE,
                  undefined,
                  new Node(
                    item.datum.name,
                    undefined,
                    item.datum.group,
                    item.datum.index,
                    undefined
                  ),
                  // @ts-ignore
                  event.clientX - HOVER_OFFSET.x,
                  // @ts-ignore
                  event.clientY - HOVER_OFFSET.y
                )
              }
            }
          })
          result.view.addEventListener("mouseout", function (_, item) {
            console.log("MOUSEOUT", item)
            hoverData = undefined
          })
        })
        .catch((error) => console.log(error))
    }
  </script>
  
  <div id="viz" />
  {#if hoverData !== undefined}
    <Hover {hoverData} />
  {/if}
  
  <style lang="scss">
    .viz {
      width: 100%;
      height: 100%;
    }
  </style>
  