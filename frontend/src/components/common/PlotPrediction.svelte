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
    x: 0,
    y: 0,
  }
  let currentNetwork: Network = $networksList[$selectedNetworkIndex]

  export let nodeData: Array<{ name: string; index: number; result: string }> =
    []
  export let edgeData: Array<{
    source: string
    target: number
    result: string
  }> = []

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
        } else if (node[task.yColumn] !== null) {
          // @ts-ignore
          if (task.predictions[node.index] === node[task.yColumn].toString()) {
            // @ts-ignore
            node.result = PredictionResult.CORRECT
          } else {
            // @ts-ignore
            node.result = PredictionResult.WRONG
          }
        }
      })

      nodeData = networkToPlot.nodes.map((node) => ({
        name: node.name,
        index: node.index,
        result: node.result,
      }))
      dispatch("nodeData", nodeData)

      updateVisSpec(networkToPlot, VisSpec)
      setColorKey(
        VisSpec,
        "nodes",
        "result",
        ["#808080", "#097969", "#FF0000"]
        //TaskType.NODE_CLASSIFICATION
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
      console.log(task.predictions)

      for (let i = 0; i < networkToPlot.links.length; i++) {
        networkToPlot.links[i].result = PredictionResult.IN_TRAIN_SET
      }
      for (const [key, value] of Object.entries(task.predictions)) {
        const [source, target] = key.split("-")

        let matchingLink
        for (let i = 0; i < networkToPlot.links.length; i++) {
          const link = networkToPlot.links[i]
          const sourceValueAsNumber = parseInt(source, 10)
          const targetValueAsNumber = parseInt(target, 10)

          if (
            link.source === sourceValueAsNumber &&
            link.target === targetValueAsNumber
          ) {
            matchingLink = link
            break
          }
        }

        if (matchingLink !== undefined) {
          // Mark this link as found in predictions
          //matchingLink.inPredictions = true

          if (value) {
            // @ts-ignore
            matchingLink.result = PredictionResult.CORRECT
          } else {
            // @ts-ignore
            matchingLink.result = PredictionResult.WRONG
          }
        } else {
          // This link was not in the original network, so we need to add it but mark it as wrong
          if (value) {
            networkToPlot.links.push({
              source: parseInt(source, 10),
              target: parseInt(target, 10),
              result: PredictionResult.WRONG,
            })
          }
        }
      }

      // Iterate through the links and set the result to IN_TRAIN for links not in predictions

      edgeData = networkToPlot.links.map((link) => ({
        source: link.source,
        target: link.target,
        result: link.result,
      }))
      dispatch("edgeData", edgeData)
      console.log("xxx")
      updateVisSpec(networkToPlot, VisSpec)
      setColorKey(
        VisSpec,
        "edges",
        "result",
        ["#097969", "#808080", "#FF0000"]
        //TaskType.EDGE_PREDICTION
      )
    }
  }

  vegaEmbed("#predictionPlot", VisSpec, { actions: false })
    .then((result) => {
      dispatch("predictionPlotLoaded", result.view)
      result.view.addEventListener("mouseover", function (event, item) {
        console.log("MOUSEOVER", item)
        const container = document.getElementById("predictionPlot")
        const containerRect = container.getBoundingClientRect()
        if (item != undefined && item.datum != undefined) {
          // @ts-ignore
          if (item != undefined && item.path != undefined) {
            // @ts-ignore
            console.log(item.path)
            hoverData = new HoverData(
              HoverType.LINK,
              item.datum,
              undefined,
              // @ts-ignore
              event.pageX + HOVER_OFFSET.x - containerRect.left,
              // @ts-ignore
              event.pageY + HOVER_OFFSET.y - containerRect.top * 0.5
            )
          } else {
            hoverData = new HoverData(
              HoverType.NODE,
              undefined,
              item.datum,
              // @ts-ignore
              event.pageX + HOVER_OFFSET.x - containerRect.left,
              // @ts-ignore
              event.pageY + HOVER_OFFSET.y - containerRect.top * 0.5
            )
          }
        }
      })
      result.view.addEventListener("mouseout", function (_, item) {
        console.log("MOUSEOUT", item)
        // hoverData = undefined
      })
    })
    .catch((error) => console.log(error))
</script>

<div id="predictionPlot" />
{#if hoverData !== undefined}
  <Hover {hoverData} />
{/if}

<!-- {#if edgeData.length > 0}
  <div id="edge_data">
    <table>
      <tr>
        <th>Source</th>
        <th>Target</th>
        <th>Result</th>
      </tr>
      {#each edgeData as edge}
        <tr>
          <td>{edge.source}</td>
          <td>{edge.target}</td>
          <td>{edge.result}</td>
        </tr>
      {/each}
    </table>
  </div>
{/if} -->

<style lang="scss">
  .viz {
    width: 100%;
    height: 100%;
  }
</style>
