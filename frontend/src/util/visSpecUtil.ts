import cloneDeep from "lodash.clonedeep"
import VisSpec from "../data/VisSpec"
import type { VisualizationSpec } from "vega-embed"
import embed from "vega-embed"
import { COLUMN_IS_TRAIN } from "../definitions/constants"
import type { Network } from "../definitions/network"
import { TaskType } from "../definitions/taskType"

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
  // @ts-ignore
  if (network.links[1]?.source?.datum !== undefined) {
    const nodeKeys = Object.keys(network.nodes[0]);
    const linkKeys = Object.keys(network.links[0]);

    visSpec.data[0].values = network.nodes.map((node) => {
      let nodeData = {};
      nodeKeys.forEach((key) => {
        nodeData[key] = node[key];
      });
      return nodeData;
    });

    visSpec.data[1].values = network.links.map((link) => {
      let linkData = {};
      linkKeys.forEach((key) => {
        if (key === 'source' || key === 'target') {
          linkData[key] = link[key].index;
        } else {
          linkData[key] = link[key];
        }
      });
      return linkData;
    });
  } else {
    visSpec.data[0].values = network.nodes
    visSpec.data[1].values = network.links
  }
  // @ts-ignore
  if (network.nodes[0].is_train != null) {
    visSpec = setColorKey(visSpec, COLUMN_IS_TRAIN, ["#ff0000", "#00ff00"])
  }
  return visSpec
}
export async function updateLinkDistance(visSpec: VisualizationSpec, newDistance) {
  let linkDistance = newDistance;
  visSpec.signals.find(signal => signal.name === 'linkDistance').value = linkDistance;
  await embed("#viz", visSpec);
}
export function setColorKey(
  visSpec: VisualizationSpec,
  target: string, // "nodes" or "edges"
  colorKey: string,
  colorPalette: string[] = undefined
): VisualizationSpec {
  if (target === "nodes") {
    const nodeScale = visSpec.scales.find((scale) => scale.name === "colorNodes");
    if (nodeScale) {
      nodeScale.domain.field = colorKey;
      if (colorPalette !== undefined) {
        nodeScale.range = colorPalette;
      }
    }
    const nodeMark = visSpec.marks.find((mark) => mark.name === "nodes");
    if (nodeMark) {
      nodeMark.encode.enter.fill.field = colorKey;
    }
  } else if (target === "edges") {
    const edgeScale = visSpec.scales.find((scale) => scale.name === "edgeColor");
    if (edgeScale) {
      edgeScale.domain.field = colorKey;
      if (colorPalette !== undefined) {
        edgeScale.range = colorPalette;
      }
    }
    const edgeMark = visSpec.marks.find((mark) => mark.name === "edges");
    if (edgeMark) {
      edgeMark.encode.update.stroke.field = colorKey;
    }
  }

  return visSpec;
}







