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

    let hoverData: HoverData = undefined
    // Run an onMount function to initialize the plot
    onMount(() => { 
        loadNetwork()
    })
  
    function loadNetwork() {
      let currentNetwork = cloneDeep($networksList[$selectedNetworkIndex])
      updateVisSpec(currentNetwork, VisSpec)
      setColorKey(VisSpec, "group", ["#FF0000", "#097969"]) // TODO: Change group to prediction
      vegaEmbed("#viz", VisSpec, { actions: false })
        .then((result) => {
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
  