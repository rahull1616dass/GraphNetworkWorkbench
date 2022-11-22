<script lang="ts">
  import { GraphFormatConverter } from "graph-format-converter"
  import { XMLParser } from "fast-xml-parser"
  import { parseNetwork } from "./networkParser"
  import type ParseResult from "papaparse"
  import type { Link } from "../../../definitions/network"
  import { Network } from "../../../definitions/network"
  import { networksList } from "../../../stores"
  import { UploadedFileType } from "../../../definitions/uploadedFileType"
  /*
   TODO Make this work with the 'File type'. Right now, this throws an eror on the bind:file if declared as 
   a File, so we use a FileList even though we will get only one file. We can be sure that we will only get one, since we do not declare
   the 'multiple' attribute on the input, as such the input only allows one file selection from the user's File Explorer.
   So with the current implementation, we assume files FileList always contain one element and thus we can index the alone file via files[0].
  */
  // Note that `files` is of type `FileList`, not an Array:
  // https://developer.mozilla.org/en-US/docs/Web/API/FileList
  let nodeFiles: FileList
  let edgeFiles: FileList
  let nodes: Node[]
  let links: Link[]

  $: if (edgeFiles) {
    let edgeFile = edgeFiles[0]
    console.log(`Selected edge file: ${edgeFile.name}: ${edgeFile.size} bytes`)
    parseFile(edgeFile, UploadedFileType.EDGE_FILE)
  }

  $: if (nodeFiles) {
    let nodeFile = nodeFiles[0]
    console.log(`Selected node file: ${nodeFile.name}: ${nodeFile.size} bytes`)
    parseFile(nodeFile, UploadedFileType.NODE_FILE)
  }

  const parseFile = (file: File, uploadedFileType: UploadedFileType) => {
    // See https://stackoverflow.com/a/66487071/11330757
    parseNetwork(file).then((parsedNetwork: ParseResult) => {
      console.log(`Parsed network: ${parsedNetwork as ParseResult}`)
      switch (uploadedFileType) {
        case UploadedFileType.NODE_FILE:
          nodes = <Node[]>JSON.parse(JSON.stringify(parsedNetwork.data))
          break
        case UploadedFileType.EDGE_FILE:
          links = <Link[]>JSON.parse(JSON.stringify(parsedNetwork.data))
          break
      }
      let networkObject: Network = new Network(
        new Array(),
        <Link[]>JSON.parse(JSON.stringify(parsedNetwork.data))
      )
      networksList.update((networksList) => {
        return [...networksList, networkObject]
      })
      console.log("x")
    })
  }


  
  /*let xmlOutput = new XMLParser().parse(files[0])
  console.log(networkSample)
  const graphmlInstance = GraphFormatConverter.fromGraphml(xmlOutput));
  console.log(graphmlInstance)
  */
</script>

<main>
  <div class="root">
    <div class="nodes_file">
      <label for="nodes_file">Upload nodes file</label>
      <input bind:files={nodeFiles} id="nodes_file" type="file" />
      {#if nodeFiles}
        <h2>Selected node file:</h2>
        <p>{nodeFiles[0].name} ({nodeFiles[0].size} bytes)</p>
      {/if}
    </div>

    <div class="edges_file">
      <label for="edges_file">Upload edges file</label>
      <input bind:files={edgeFiles} id="edges_file" type="file" />
      {#if nodeFiles}
        <h2>Selected edge file:</h2>
        <p>{nodeFiles[0].name} ({nodeFiles[0].size} bytes)</p>
      {/if}
    </div>

    {#if $networksList.length > 0}
      <p>Network element at position 0 is {$networksList[0].links}</p>
    {/if}
  </div>

</main>

<style>
  .root {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
  }
</style>
