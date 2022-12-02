<script lang="ts">
  import { GraphFormatConverter } from "graph-format-converter"
  import { XMLParser } from "fast-xml-parser"
  import { parseNetwork } from "./networkParser"
  import type ParseResult from "papaparse"
  import type { Link, Metadata } from "../../../definitions/network"
  import type { Node } from "../../../definitions/network"
  import { Network } from "../../../definitions/network"
  import { ModalData } from "../../../definitions/modalData"
  import { MenuItem } from "../../../definitions/menuItem"
  import {
    selectedMenuItem,
    networksList,
    paletteColors,
  } from "../../../stores"
  import { UploadedFileType } from "../../../definitions/uploadedFileType"
  import {
    Button,
    Modal,
    TextInput,
    FileUploader,
  } from "carbon-components-svelte"
  import { Palette } from "@untemps/svelte-palette"
  import cryptoRandomString from "crypto-random-string"

  let modalData: ModalData = new ModalData()
  /*
   TODO Make this work with the 'File type'. Right now, this throws an eror on the bind:file if declared as 
   a File, so we use a FileList even though we will get only one file. We can be sure that we will only get one, since we do not declare
   the 'multiple' attribute on the input, as such the input only allows one file selection from the user's File Explorer.
   So with the current implementation, we assume files FileList always contain one element and thus we can index the alone file via files[0].
  */
  // Note that `files` is of type `FileList`, not an Array:
  // https://developer.mozilla.org/en-US/docs/Web/API/FileList

  
  let idPlaceHolder = cryptoRandomString({length: 4, type: 'url-safe'})
  $: idPlaceHolder = idPlaceHolder.replace (/^/,newNetwork.metadata.name);

  // TODO OnClose callback doesn't work for now
  let nodeFiles: File[] = []
  let edgeFiles: File[] = []
  let newNetwork = new Network()
  let isUploadComplete = false



  $: if (edgeFiles.length > 0) {
    let edgeFile = edgeFiles[0]
    console.log(`Selected edge file: ${edgeFile.name}: ${edgeFile.size} bytes`)
    parseFile(edgeFile, UploadedFileType.EDGE_FILE)
  }

  $: if (nodeFiles.length > 0) {
    let nodeFile = nodeFiles[0]
    console.log(`Selected node file: ${nodeFile.name}: ${nodeFile.size} bytes`)
    parseFile(nodeFile, UploadedFileType.NODE_FILE)
  }

  function parseFile(file: File, uploadedFileType: UploadedFileType) {
    // See https://stackoverflow.com/a/66487071/11330757
    parseNetwork(file).then((parsedNetwork: ParseResult) => {
      console.log(`Parsed network: ${parsedNetwork as ParseResult}`)
      switch (uploadedFileType) {
        case UploadedFileType.NODE_FILE:
          newNetwork.nodes = <Node[]>(
            JSON.parse(JSON.stringify(parsedNetwork.data))
          )
          break
        case UploadedFileType.EDGE_FILE:
          newNetwork.links = <Link[]>(
            JSON.parse(JSON.stringify(parsedNetwork.data))
          )
          break
      }
    })
  }

  function onSaveButtonClicked() {
    console.log(
      `Save button clicked with nodes: ${newNetwork.nodes} and edges: ${newNetwork.links}`
    )
    if (newNetwork.nodes.length == 0) {
      modalData.messageBody = "Please upload a valid nodes file."
      modalData.isOpen = true
      return
    }
    if (newNetwork.links.length == 0) {
      modalData.messageBody = "Please upload a valid edges file."
      modalData.isOpen = true
      return
    }
    networksList.update((networksList) => {
      return [...networksList, newNetwork]
    })

    //TODO Newline does not render in the modal currently.
    modalData.messageBody = `Network successfully uploaded.\nName: ${newNetwork.metadata.name}
                            \nDescription: ${newNetwork.metadata.description}
                            \nNodes: ${newNetwork.nodes.length} \nEdges: ${newNetwork.links.length}`
    modalData.isOpen = true
    isUploadComplete = true
    console.log("x")
  }

  function onModalClose() {
    if (isUploadComplete) {
      $selectedMenuItem = MenuItem.HOME
    }
  }
  /*let xmlOutput = new XMLParser().parse(files[0])
  console.log(networkSample)
  const graphmlInstance = GraphFormatConverter.fromGraphml(xmlOutput));
  console.log(graphmlInstance)
  */
</script>

<main>
  <div class="root">
    <div class="metadata">
      <div class="metadata_title">
        <TextInput
          bind:value={newNetwork.metadata.name}
          type="text"
          id="network-name"
          labelText="Network Name"
        />
        <div class="metadata_id">
          <TextInput
            bind:value={newNetwork.metadata.id}
            type="text"
            bind:placeholder={idPlaceHolder}
            id="network-id"
            labelText="A unique network ID"
          />
        </div>
      </div>
      <div class="metadata_description">
        <TextInput
          bind:value={newNetwork.metadata.description}
          type="text"
          id="network-description"
          labelText="Network Description"
        />
        <div class="palette">
          <div class="labels">Network Color</div>
          <Palette
            colors={$paletteColors}
            on:select={({ detail: { color } }) =>
              (newNetwork.metadata.color = color)}
          />

          <div class="nodes_file">
            <FileUploader
              labelTitle="Upload nodes file"
              buttonLabel="Add file"
              status="complete"
              bind:files={nodeFiles}
            />
            <!--
      {#if nodeFiles.length > 0}
        <h2>Selected node file:</h2>
        <p>{nodeFiles[0].name} ({nodeFiles[0].size} bytes)</p>
      {/if}
      -->
          </div>

          <div class="edges_file">
            <FileUploader
              labelTitle="Upload edges file"
              buttonLabel="Add file"
              status="complete"
              bind:files={edgeFiles}
            />
            <!--
      {#if edgeFiles.length > 0}
        <h2>Selected edge file:</h2>
        <p>{edgeFiles[0].name} ({edgeFiles[0].size} bytes)</p>
      {/if}
      -->
          </div>

          <div class="save_button">
            <Button on:click={onSaveButtonClicked}>Save Network</Button>
          </div>

          {#if modalData.isOpen}
            <Modal
              passiveModal
              bind:open={modalData.isOpen}
              modalHeading={modalData.messageHeader}
              on:open
              on:close={onModalClose}
            >
              {modalData.messageBody}
            </Modal>
          {/if}
        </div>
      </div>
    </div>
  </div>
</main>

<style>
  .root {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
  }

  .metadata {
    margin: 1rem;
  }

  .palette {
    margin-top: 1rem;
  }

  .labels {
    text-align: left;
  }

  .save_button {
    margin-top: 1rem;
  }
</style>
