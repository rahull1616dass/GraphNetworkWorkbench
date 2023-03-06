import JSZip from 'jszip'
import { Network } from "../../../definitions/network"
import { uploadNetworkToStorage } from "../../../api/firebase"
import type { Link, Node } from "../../../definitions/network"
import { NetworkImportStates } from '../../../definitions/ImportNetworkStates'

export let uploadedNetworkStatus: NetworkImportStates
  function UploadTheData(nodes, edges, network){
    console.log(nodes)
    console.log(edges)
      let nodesFile = new File([nodes], "Nodes.csv", { type: "text/csv" })
      let edgesFile = new File([edges], "Edges.csv", { type: "text/csv" })
      
      network.nodes = <Node[]>(
            JSON.parse(JSON.stringify(nodes))
          )
      network.links = <Link[]>(
            JSON.parse(JSON.stringify(edges))
          )
      return uploadNetworkToStorage(
      network.metadata,
      nodesFile,
      edgesFile
    )
  }

export async function onFetchNetwork(event) {
    
    uploadedNetworkStatus = NetworkImportStates.DownloadingNetwork;
    fetch(`https://us-central1-graphlearningworkbench.cloudfunctions.net/downloadNetworkFile?networkName=${event.detail.networkName}`)
    .then(response => response.blob())
    .then(blob =>{
        uploadedNetworkStatus = NetworkImportStates.ImportingNetwork
      return JSZip.loadAsync(blob)
    })
    .then(zip =>{ 
      let edgeFile
      let nodeFile
      edgeFile = zip.files['edges.csv'].async('text')
      nodeFile = zip.files['nodes.csv'].async('text')
      return Promise.all([edgeFile , nodeFile])
    })
    .then(alltext =>{
      
      let nodesString = removeCSVColumns(alltext[1].replace('# ',''), [' name',' _pos'])
      let edgesString = alltext[0].replace('# ','')
      let network = new Network();
      network.metadata.name = event.detail.networkName
      network.metadata.description = event.detail.content.description
      network.metadata.id = event.detail.networkName
      network.metadata.color = ""
      return UploadTheData(nodesString, edgesString, network)
    })
    .then(url => {
      console.log(`Network uploaded to ${url}`)
      uploadedNetworkStatus = NetworkImportStates.NetworkImported;
    })

  }

  function removeCSVColumns(csvData, columnsToRemove) {
    const rows = csvData.split("\n").map(row => {
      const cells = [];
      let cell = "";
      let insideQuote = false;
      for (const char of row) {
        if (char === '"') {
          insideQuote = !insideQuote;
        } else if (char === "," && !insideQuote) {
          cells.push(cell);
          cell = "";
        } else {
          cell += char;
        }
      }
      cells.push(cell);
      return cells;
    });
    const header = rows[0];
    let indicesToRemove = [];
    if (Array.isArray(columnsToRemove)) {
      for (const col of columnsToRemove) {
        const index = header.indexOf(col);
        if (index !== -1) {
          indicesToRemove.push(index);
        }
      }
    }
    return rows.map(row => {
      return row.filter((_, i) => !indicesToRemove.includes(i));
    }).map(row => row.join(",")).join("\n");
  }