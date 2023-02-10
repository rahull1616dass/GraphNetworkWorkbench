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

  export let seed: number = 0
  export let trainPercentage: number = 0.8
  let hoverData: HoverData = undefined
  let currentNetwork: Network = undefined
  const dispatcher = createEventDispatcher()

  // Run an onMount function to initialize the plot
  onMount(() => {
    loadNetwork(true)
  })

  function loadNetwork(isFirstLoad: boolean = false) {
    if (isFirstLoad) {
      currentNetwork = cloneDeep($networksList[$selectedNetworkIndex])
      currentNetwork = train_test_split(currentNetwork, seed, trainPercentage)
    }
    updateVisSpec(currentNetwork, VisSpec)
    if (isFirstLoad) {
      setColorKey(VisSpec, "is_train")
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
                currentNetwork.nodes[item.datum.index].is_train
              }`
            )
            let newValue: number
            // See experimentUtils.ts for the meaning of the values
            if (item.datum.is_train === 1) {
              newValue = 2
            } else {
              newValue = 1
            }
            currentNetwork.nodes[item.datum.index].is_train = newValue
            console.log(
              `For node ${item.datum.name} is_train = ${
                currentNetwork.nodes[item.datum.index].is_train
              }`
            )
            loadNetwork(false)
          }
        })
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
                event.clientX,
                // @ts-ignore
                event.clientY
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
                event.clientX,
                // @ts-ignore
                event.clientY
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

<CustomModal on:close>
  <h4 slot="header">Customize Train/Test Split</h4>
  <div slot="body">
    <div id="viz" />
    {#if hoverData !== undefined}
      <Hover {hoverData} />
    {/if}
  </div>

  <div slot="footer">
    <CustomButton
      type={"primary"}
      inverse={true}
      on:click={() => {
        dispatcher("onSaveSplitClicked", currentNetwork)
      }}
    >
      Save
    </CustomButton>

    <CustomButton
      type={"delete"}
      inverse={true}
      on:click={() => {
        loadNetwork(true)
      }}
    >
      Cancel
    </CustomButton>
  </div>
</CustomModal>

<style lang="scss">
  .viz {
    width: 100%;
    height: 100%;
  }
</style>
