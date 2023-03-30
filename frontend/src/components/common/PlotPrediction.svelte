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
  import { TaskType } from "../../definitions/taskType"

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

    /*
    We check the purpose of creating this prediction plot. 
    
    If the plot is created to show the results of node classification, then each node's color needs 
    to be adjusted, depending on whether it was
    in the training set, or if it was correctly or incorrectly classified. 
    
    If the plot is created to show the results of link prediction, 
    */
    if (task.taskType === TaskType.NODE_CLASSIFICATION) {
       /*
        In this case, the structure of task.predictions is supposed to be:
        {
            "{node_index}": "{predicted_class}"
        }
       */
      networkToPlot.nodes.forEach((node) => {
        // If node.index is not in predictions, then that node was in the training set
        // @ts-ignore
        if (task.predictions[node.index] === undefined) {
          // @ts-ignore
          node.result = PredictionResult.IN_TRAIN_SET
        } else if (
          // @ts-ignore
          task.predictions[node.index] === node[task.yColumn].toString()
        ) {
          // @ts-ignore
          node.result = PredictionResult.CORRECT
        } else {
          // @ts-ignore
          node.result = PredictionResult.WRONG
        }
      })

      updateVisSpec(networkToPlot, VisSpec)
      setColorKey(
        VisSpec,
        "result",
        ["#808080", "#FF0000", "#097969"],
        TaskType.NODE_CLASSIFICATION
      )
    } else if (task.taskType === TaskType.EDGE_PREDICTION) {
      /*
        In this case, the structure of task.predictions is supposed to be:
        {
            "{source}-{target}": "{boolean value of whether the prediction was correct}"
        }
        Note that there could be edges here that are not in the original network. In this case it should always
        be the case that the prediction is false.
        Any edges that are in the original network but not in the predictions should be assumed to be 
        in the training set and thus labeled grey.
        */

      /* For each key in the predictions object, we need to check if the edge is in the original network.
        If it is, then we need to check if the prediction was correct or not. If it is not, then we need to
        add it to the network and label it as wrong.
        */
      for (const [key, value] of Object.entries(task.predictions)) {
        const [source, target] = key.split("-")
        const link = networkToPlot.links.find((link: Link) =>
          link.equals(new Link(source, target))
        )
        if (link !== undefined) {
          if (value) {
            // @ts-ignore
            link.result = PredictionResult.CORRECT
          } else {
            // @ts-ignore
            link.result = PredictionResult.WRONG
          }
        } else {
          networkToPlot.links.push({
            source: source,
            target: target,
            result: PredictionResult.WRONG,
          })
        }
      }
    }
    updateVisSpec(networkToPlot, VisSpec)
    setColorKey(
      VisSpec,
      "result",
      ["#808080", "#FF0000", "#097969"],
      TaskType.EDGE_PREDICTION
    )
  }

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
