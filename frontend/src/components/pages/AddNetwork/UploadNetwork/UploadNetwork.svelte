<script lang="ts">
  import { GraphFormatConverter } from "graph-format-converter"
  import { XMLParser } from "fast-xml-parser"
  import { parseNetwork, toCSVFile } from "../../../../util/networkParserUtil"
  import type ParseResult from "papaparse"
  import { Network, Node, Link, Metadata } from "../../../../definitions/network"
  import { ModalData } from "../../../../definitions/modalData"
  import { MenuItem } from "../../../../definitions/menuItem"
  import {
    selectedMenuItem,
    networksList,
    paletteColors,
  } from "../../../../stores"
  import { UploadedFileType } from "../../../../definitions/uploadedFileType"
  import { Modal, TextInput, ProgressBar } from "carbon-components-svelte"
  import { Palette } from "@untemps/svelte-palette"
  import cryptoRandomString from "crypto-random-string"
  import { uploadNetworkToStorage } from "../../../../api/firebase"
  import { ProgressBarData } from "../../../../definitions/progressBarData"
  import { onMount } from "svelte"
  import CustomInput from "../../../common/CustomInput.svelte"
  import CustomButton from "../../../common/CustomButton.svelte"
  import InfoBox from "../../../common/InfoBox.svelte"
  import { fade, slide, scale, fly } from "svelte/transition"

  onMount(() => {
    /*
    Once the user selects an import type from the modal, the selectedImportType is changed to 
    something other than NONE.
    At this point, the selectedMenuItem must be set to NONE so that the root div is not rendered
    on top of the import pages
    */
    $selectedMenuItem = MenuItem.FROM_PC
  })

  let modalData: ModalData = new ModalData()
  let progressBarData: ProgressBarData = new ProgressBarData()
  $: isInfoModalOpen = false

  /*
   TODO Make this work with the 'File type'. Right now, this throws an eror on the bind:file if declared as 
   a File, so we use a FileList even though we will get only one file. We can be sure that we will only get one, since we do not declare
   the 'multiple' attribute on the input, as such the input only allows one file selection from the user's File Explorer.
   So with the current implementation, we assume files FileList always contain one element and thus we can index the alone file via files[0].
  */
  // Note that `files` is of type `FileList`, not an Array:
  // https://developer.mozilla.org/en-US/docs/Web/API/FileList

  // TODO OnClose callback doesn't work for now
  let nodeFiles: File[] = []
  let edgeFiles: File[] = []
  let newNetwork = new Network(new Metadata())
  
  let randomId = cryptoRandomString({ length: 4, type: "url-safe" })
  $: newNetwork.metadata.id = `${newNetwork.metadata.name}-${randomId}`

  let isUploadSuccessful = false

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

  $: isSaveButtonDisabled = newNetwork.metadata.name === "" || newNetwork.links.length === 0 || newNetwork.nodes.length === 0

  function parseFile(file: File, uploadedFileType: UploadedFileType) {
    // See https://stackoverflow.com/a/66487071/11330757
    parseNetwork(file).then((parseResult: ParseResult) => {
      console.log(`Parsed network: ${parseResult as ParseResult}`)
      switch (uploadedFileType) {
        case UploadedFileType.NODE_FILE:
          if (!parseResult.meta.fields.includes("name")) {
            onInvalidFile(
              `'name' field is required for nodes. Please create this column 
            in your nodes file and assign a name to each node.
            `,
              UploadedFileType.NODE_FILE
            )
            return
          }
          if (!parseResult.meta.fields.includes("index")) {
            parseResult.data.forEach((value, index) => {
              value["index"] = index
            })
            parseResult.meta.fields.push("index")
          }
          newNetwork.nodes = parseResult.data
          checkForExtraField(newNetwork.nodes, UploadedFileType.NODE_FILE)
          break
        case UploadedFileType.EDGE_FILE:
          let isFileValid = true
          const requiredColumns = ["source", "target"]
          requiredColumns.forEach((column) => {
            if (!parseResult.meta.fields.includes(column)) {
              onInvalidFile(
                `'${column}' field is required for edges. Please create this column and assign a 
              ${column} to each edge.`,
                UploadedFileType.EDGE_FILE
              )
              isFileValid = false
              return
            }
            if (!isFileValid) return
          })
          newNetwork.links = <Link[]>(
            JSON.parse(JSON.stringify(parseResult.data))
          )
          checkForExtraField(newNetwork.links, UploadedFileType.EDGE_FILE)
          break
      }
    })
  }

  function checkForExtraField(
    list: object[],
    uploadedFileType: UploadedFileType
  ) {
    list.forEach((element) => {
      //@ts-ignore
      if (element.__parsed_extra !== undefined) {
        switch (uploadedFileType) {
          case UploadedFileType.NODE_FILE:
            /*
            onInvalidFile(
              `The node ${element.name} has an extra column that is not part of the network. 
              Please remove this column from the nodes file.`,
              UploadedFileType.NODE_FILE
            )
            */
            break
          case UploadedFileType.EDGE_FILE:
            onInvalidFile(
              `The edge Index_${element.source} -> Index_${element.target} has an extra column that 
              is not part of the network. Please remove this column from the edges file.`,
              UploadedFileType.EDGE_FILE
            )
            break
        }
      }
    })
  }

  function onInvalidFile(
    messageBody: string,
    uploadedFileType: UploadedFileType
  ) {
    modalData.messageBody = messageBody
    modalData.isOpen = true
    switch (uploadedFileType) {
      case UploadedFileType.NODE_FILE:
        nodeFiles = []
        newNetwork.nodes = []
        break
      case UploadedFileType.EDGE_FILE:
        edgeFiles = []
        newNetwork.links = []
        break
    }
  }

  function onSaveButtonClicked() {
    progressBarData.isPresent = true
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

    /*
    One could also store the network in each user's Firestore document, and this would even
    work well as it integrates directly with the network class that we defined.
    However, a document has a size limit of 1MB: https://firebase.google.com/docs/firestore/quotas
    While this should be enough for most networks, if we are going to have a prodcution-ready
    application, it is better to store the networks in Firebase Storage, and only store the
    metadata in Firestore. This way, we can have a much larger network size limit.
    */
    uploadNetworkToFirebaseStorage()
  }

  async function uploadNetworkToFirebaseStorage() {
    progressBarData.text = "Saving network to the cloud..."
    /*
    Why create the CSV file from scratch using the newNetwork object, rather than simply
    uploading the files that the user uploaded? 
    This is because the user may have uploaded a file that has extra 
    columns that are not part of the network. We want to remove these
    extra columns before uploading the network to Firebase Storage. Or it could be that the
    index was missing and it was added by the client. In these cases, the user's file
    is not the same as the network that we want to upload.
    */
    let files: Record<string, File> = newNetwork.toFiles()
    await uploadNetworkToStorage(newNetwork.metadata, files.nodes, files.links)
      .then((url) => {
        console.log(`Network uploaded to ${url}`)
        //TODO Newline does not render in the modal currently.
        modalData.messageBody = `Network successfully uploaded.\nName: ${newNetwork.metadata.name}
                            \nDescription: ${newNetwork.metadata.description}
                            \nNodes: ${newNetwork.nodes.length} \nEdges: ${newNetwork.links.length}`
        modalData.isOpen = true
        isUploadSuccessful = true
        progressBarData.isPresent = false
      })
      .catch((error) => {
        console.log(`Error uploading network: ${error}`)
        modalData.messageBody = `Oops... Something went wrong\nError uploading network`
        modalData.isOpen = true
        isUploadSuccessful = false
        progressBarData.isPresent = false
      })
  }

  function onModalClose() {
    if (isUploadSuccessful) {
      $selectedMenuItem = MenuItem.HOME
    }
  }
  /*let xmlOutput = new XMLParser().parse(files[0])
  console.log(networkSample)
  const graphmlInstance = GraphFormatConverter.fromGraphml(xmlOutput));
  console.log(graphmlInstance)
  */
</script>

<div
  in:fly={{ y: -50, duration: 250, delay: 300 }}
  out:fly={{ y: -50, duration: 250 }}
  class="root"
>
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
          disabled
          type="text"
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
          selectedColor={$paletteColors[Math.floor(Math.random() * $paletteColors.length)]}
          on:select={({ detail: { color } }) =>
            (newNetwork.metadata.color = color)}
        />
      </div>
    </div>

    <div class="grid">
      <div>
        <CustomInput id="nodeFile" bind:files={nodeFiles}
          >Upload Node File</CustomInput
        >
      </div>
      <div class="info">
        <InfoBox
          bind:isInfoModalOpen
          headerText="File Guide"
          bodyText="Currently, only csv files are supported. It is required that the
        network consists of two files:  
         - nodes.csv 
         - edges.csv 
        Each file has to have a header row which contains the column names. There
        are special column names, that may be required or may have a special function
        assigned to them (see below). Other than that, the user is free to add
        any number of additional columns with arbitrary names that will function
        as node or edge features depending on the file. <br /> <br />
        The nodes.csv file must contain either 'name' or 'index', or both. If the
        nodes are not named, then the user must provide at least the index column
        where each row is assigned a unique index from 0 to n-1 where n is the
        number of nodes. If the name column is present, then the index column is
        optional as this can be automatically generated from each row's position.
        'name' is a special column and if present, it will be shown as the node's
        name in the Visualize page when the node is hovered on. <br /> 'group'
        is another special column that can be used to assign a group to each
        node. Visualize page will then color the nodes according to their
        group. <br /> <br /> The edges.csv file must contain the 'source' and 'target'
        columns that specify which nodes the edge connects to. Currently only undirected
        edges are supported in the Visualize Page, although the specific ordering
        can be relevant for the machine learning algorithms that run on the network.
        Note that 'source' and 'target' must be integers that correspond to the
        indices of nodes as either explicitly specified in the nodes.csv file or
        automatically generated from the nodes.csv file."
        />
      </div>
      <div>
        <CustomInput id="edgeFile" bind:files={edgeFiles}
          >Upload Edge File</CustomInput
        >
      </div>
      <div class="info">
        <InfoBox
          bind:isInfoModalOpen
          headerText="File Guide"
          bodyText="Currently, only csv files are supported. It is required that the
        network consists of two files:  
         - nodes.csv 
         - edges.csv 
        Each file has to have a header row which contains the column names. There
        are special column names, that may be required or may have a special function
        assigned to them (see below). Other than that, the user is free to add
        any number of additional columns with arbitrary names that will function
        as node or edge features depending on the file. <br /> <br />
        The nodes.csv file must contain either 'name' or 'index', or both. If the
        nodes are not named, then the user must provide at least the index column
        where each row is assigned a unique index from 0 to n-1 where n is the
        number of nodes. If the name column is present, then the index column is
        optional as this can be automatically generated from each row's position.
        'name' is a special column and if present, it will be shown as the node's
        name in the Visualize page when the node is hovered on. <br /> 'group'
        is another special column that can be used to assign a group to each
        node. Visualize page will then color the nodes according to their
        group. <br /> <br /> The edges.csv file must contain the 'source' and 'target'
        columns that specify which nodes the edge connects to. Currently only undirected
        edges are supported in the Visualize Page, although the specific ordering
        can be relevant for the machine learning algorithms that run on the network.
        Note that 'source' and 'target' must be integers that correspond to the
        indices of nodes as either explicitly specified in the nodes.csv file or
        automatically generated from the nodes.csv file."
        />
      </div>
    </div>

    {#if progressBarData.isPresent}
      <div class="progress_bar">
        <ProgressBar helperText={progressBarData.text} />
      </div>
    {:else}
      <div class="save_button">
        <CustomButton
          type={"secondary"}
          inverse={false}
          disabled={isSaveButtonDisabled}
          on:click={onSaveButtonClicked}>Save Network</CustomButton
        >
      </div>
    {/if}
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

<style>
  .grid {
    display: grid;
    grid-template-columns: 4fr 1fr;
    grid-template-rows: repeat(2, 1fr);
    grid-gap: 1%;
  }
  .info {
    display: flex;
  }
  .root {
    display: absolute;
    align-items: center;
    width: 40%;
    align-content: center;
    margin: auto;
  }

  .metadata {
    margin: 1rem;
  }

  .infobox {
    border: 1px solid var(--dark-gray);
    padding: 1rem;
    margin: 1rem;
  }

  .palette {
    margin-top: 1rem;
  }

  .labels {
    text-align: left;
  }

  .save_button {
    padding-top: 10%;
  }
</style>
