<script lang="ts">
  import { GraphFormatConverter } from "graph-format-converter"
  import networkSample from "./networkSample"
  import { XMLParser } from "fast-xml-parser"
  import { parseNetwork } from "./networkParser"
  import type ParseResult from "papaparse"

  /*
   TODO Make this work with the 'File type'. Right now, this throws an eror on the bind:file if declared as 
   a File, so we use a FileList even though we will get only one file. We can be sure that we will only get one, since we do not declare
   the 'multiple' attribute on the input, as such the input only allows one file selection from the user's File Explorer.
   So with the current implementation, we assume files FileList always contain one element and thus we can index the alone file via files[0].
  */
  let files: FileList
  let networkElement

  $: if (files) {
    // Note that `files` is of type `FileList`, not an Array:
    // https://developer.mozilla.org/en-US/docs/Web/API/FileList
    console.log(files)
    for (const file of files) {
      console.log(`${file.name}: ${file.size} bytes`)
    }
    console.log("parse")
    // See https://stackoverflow.com/a/66487071/11330757
    console.log("Parsing network...")
    parseNetwork(files[0])
        .then((network: ParseResult) => {
      console.log(`Parsed network: ${network as ParseResult}`)
      networkElement = JSON.stringify(network.data[0])
    })
  }

  /*let xmlOutput = new XMLParser().parse(files[0])
  console.log(networkSample)
  const graphmlInstance = GraphFormatConverter.fromGraphml(xmlOutput));
  console.log(graphmlInstance)
  */
</script>

<main>
  <label for="many">Upload multiple files of any type:</label>
  <input bind:files id="many" type="file" />

  {#if files}
    <h2>Selected files:</h2>
    {#each Array.from(files) as file}
      <p>{file.name} ({file.size} bytes)</p>
    {/each}
  {/if}
  <p>Network element at position 0 is {networkElement}</p>
</main>

<style>
</style>
