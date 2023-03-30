<script lang="ts">
  import { selectedNetworkIndex, networksList } from "../../stores"
  import { default as vegaEmbed } from "vega-embed"
  import VisSpec from "../../data/VisSpec"
  import { updateVisSpec, setColorKey } from "../../util/visSpecUtil"
  import { onMount } from "svelte"
  import { train_test_split } from "../../util/experimentUtil"
  import type { Network } from "../../definitions/network"
  import { Node, Link } from "../../definitions/network"
  import cloneDeep from "lodash.clonedeep"
  import { HoverData } from "../../definitions/hoverData"
  import Hover from "../pages/Workbench/Plot/Hover.svelte"
  import { HoverType } from "../../definitions/hoverType"
  import CustomButton from "./CustomButton.svelte"
  import { createEventDispatcher } from "svelte"
  import CustomModal from "./CustomModal.svelte"
  import PlotPrediction from "./PlotPrediction.svelte"
  import { COLUMN_IS_TRAIN } from "../../definitions/constants"

  export let seed: number = 0
  export let trainPercentage: number = 0.8
  export let currentNetwork: Network = undefined
  let networkToUpdate: Network = undefined
  export let nameColumn: string = "name"
  export let groupColumn: string = "group"
  let hoverData: HoverData = undefined


  let shouldCheckSplits: boolean = false
  const groupSplits = {}
  let isTrainTestSplitValid: boolean = false

  $: if (shouldCheckSplits === true) {
    // Get all the unique values in currentNetwork.nodes[groupColumn]
    const uniqueGroups = Array.from(
      new Set(networkToUpdate.nodes.map((node) => node[groupColumn]))
    )
    isTrainTestSplitValid = uniqueGroups.every((group) => {
      const nodesInGroup = networkToUpdate.nodes.filter(
        (node) => node[groupColumn] == group
      )
      const nodesInGroupTrain = nodesInGroup.filter(
        (node) => node[COLUMN_IS_TRAIN] == true
      )
      const nodesInGroupTest = nodesInGroup.filter(
        (node) => node[COLUMN_IS_TRAIN] == false
      )
      groupSplits[group] = {
        train: nodesInGroupTrain.length,
        test: nodesInGroupTest.length,
      }
      return nodesInGroupTrain.length > 0 && nodesInGroupTest.length > 0
    })
    shouldCheckSplits = false
  }
  const HOVER_PIXEL_OFFSETY: number = 200
  const HOVER_PIXEL_OFFSETX: number = 50
  const dispatcher = createEventDispatcher()

  // Run an onMount function to initialize the plot
  onMount(() => {
    loadNetwork(true)
    shouldCheckSplits = true
  })

  function loadNetwork(isFirstLoad: boolean = false) {
    if (isFirstLoad) {
      networkToUpdate = cloneDeep(currentNetwork)
      networkToUpdate = train_test_split(networkToUpdate, seed, trainPercentage)
    }
    updateVisSpec(networkToUpdate, VisSpec)
    if (isFirstLoad) {
      setColorKey(VisSpec, COLUMN_IS_TRAIN)
    }
    vegaEmbed("#viz", VisSpec, { actions: false })
      .then((result) => {
        result.view.addEventListener("click", function (_, item) {
          console.log("CLICK", item)
          // @ts-ignore
          if (item.path !== undefined) {
            // Link clicked, pass
          } else {
            console.log(
              `For node ${item.datum.name} is_train = ${
                // @ts-ignore
                networkToUpdate.nodes[item.datum.index].is_train
              }`
            )
            // @ts-ignore
            networkToUpdate.nodes[item.datum.index].is_train = !networkToUpdate.nodes[item.datum.index].is_train
            console.log(
              `For node ${item.datum.name} is_train = ${
                // @ts-ignore
                networkToUpdate.nodes[item.datum.index].is_train
              }`
            )
            loadNetwork(false)
            shouldCheckSplits = true
          }
        })
        result.view.addEventListener("mouseover", function (event, item) {
          console.log("MOUSEOVER", item)
          const container = document.getElementById("viz");
          const containerRect = container.getBoundingClientRect();
          if (item != undefined && item.datum != undefined) {
            // @ts-ignore
            if (item != undefined && item.path != undefined) {
              /*
              Link is hovered. Since we do not support ML tasks that train with the links,
              the link is not clickable and we do not show any hover data.
              */
            } else {
              hoverData = new HoverData(
                HoverType.NODE,
                undefined,
                new Node(
                  item.datum[nameColumn],
                  undefined,
                  item.datum[groupColumn],
                  item.datum.index,
                  undefined,
                  // @ts-ignore
                  networkToUpdate.nodes[item.datum.index].is_train
                ),
                // @ts-ignore
                event.pageX + HOVER_PIXEL_OFFSETX - containerRect.left,
                // @ts-ignore
                event.pageY + HOVER_PIXEL_OFFSETY - containerRect.top
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

<CustomModal on:close={() => dispatcher("closePopup") }>
  <h4 slot="header">Customize Train/Test Split</h4>
  <div slot="body">
    <div class="info">
      <p>Green nodes: Test set</p><br />
      <p>Red nodes: Training set</p>
        Click on the nodes to change their training status. The color of the
        nodes will change to reflect the new status.
    </div>
    <div class="condition">
      For each of the unique value in the <b>{groupColumn}</b> column (the column you selected to 
      be predicted), there has to be at least one node in the training set and one node in the test set.
      {#each Object.entries(groupSplits) as [group, groupSplit]}
        <p>Group {group}: {groupSplit.train} nodes in training set, {groupSplit.test} nodes in test set.</p>
      {/each}
      <p>Currently this condition is <b>{isTrainTestSplitValid ? "met" : "not met"}</b>.</p>
    </div>
    <div id="viz" />

    {#if hoverData !== undefined}
      <Hover {hoverData} />
    {/if}
  </div>

  <div slot="footer">
    <CustomButton
      type={"secondary"}
      inverse={false}
      disabled={!isTrainTestSplitValid}
      on:click={() => {
        dispatcher("saveSplitClicked", { network: networkToUpdate })
      }}
    >
      Save
    </CustomButton>

    <CustomButton
      type={"delete"}
      inverse={false}
      on:click={() => {
        loadNetwork(true)
      }}
    >
      Discard Changes
    </CustomButton>
  </div>
</CustomModal>

<style lang="scss">
  .viz {
    width: 100%;
    height: 100%;
  }
</style>
