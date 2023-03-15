import cloneDeep from "lodash.clonedeep"
import VisSpec from "../data/VisSpec"
import type { VisualizationSpec } from "vega-embed"
import type { Network } from "../definitions/network"

export function updateVisSpec(
  network: Network,
  visSpec: VisualizationSpec
): VisualizationSpec {
  /*
    There was a nasty bug with the previous network's data still being visible in the new network,
    whenever the network was updated (for instance the links would stay in their previous positions
    thus not being connected to any of its nodes which already changed positions). 
    This was because the visualization related data was not being reset. Tried several things to fix this, including
    using vega's own functions such as view.data() and view.change() with changeSet but none of them worked.
    Hence this slightly hacky solution. 
    Once vegaEmbed generates a visualization, it attaches some extra data to the network object
    such as the position of the nodes and links.
    This data is not present in the network object when the network is first loaded.
    Therefore by checking if one of the properties is present, we can determine if the network has been generated before.
    This resets the previous data and allows them to be re-generated according to the updated data.
    */
  console.log("what do i do ", network.links[1].source.datum !== undefined)
  // @ts-ignore
  if (network.links[1].source.datum !== undefined) {
    visSpec.data[0].values = network.nodes.map((node) => {
      return {
        name: node.name,
        group: node.group,
        index: node.index,
        is_train: node.is_train,
      }
    })
    visSpec.data[1].values = network.links.map((link) => {
      return {
        // @ts-ignore
        source: link.source.index,
        // @ts-ignore
        target: link.target.index,
        value: link.value,
      }
    })
  } else {
    visSpec.data[0].values = network.nodes
    visSpec.data[1].values = network.links
  }
  if(network.nodes[0].is_train !== undefined){
    visSpec = setColorKey(visSpec, COLUMN_IS_TRAIN, ["#ff0000", "#00ff00"])
  }
  return visSpec
}

export function setColorKey(
  visSpec: VisualizationSpec,
  colorKey: string,
  colorPalette: string[] = undefined
): VisualizationSpec {
  /*
  Set what key to use for coloring the nodes.
  */

  // @ts-ignore
  visSpec.scales[0].domain.field = colorKey
  if (colorPalette !== undefined) {
    // @ts-ignore
    visSpec.scales[0].range = colorPalette
  }
  // @ts-ignore
  visSpec.marks[0].encode.enter.fill.field = colorKey
  return visSpec
}
