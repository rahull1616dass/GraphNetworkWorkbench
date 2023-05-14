<script lang="ts">
  import { DataTable } from "carbon-components-svelte"
  import DropdownSelector from "../../common/DropdownSelector.svelte"
  import { DropdownSelectorType } from "../../../definitions/dropdownSelectorType"
  import { selectedNetworkIndex, networksList } from "../../../stores"
  import { getExperimentTasks } from "../../../api/firebase"
  import type { Task } from "../../../definitions/task"
  import { ModalData } from "../../../definitions/modalData"
  import { fly } from "svelte/transition"
  import CustomButton from "../../common/CustomButton.svelte"
  import ExperimentResults from "../../common/ExperimentResults.svelte"
  import InfoBox from "../../common/InfoBox.svelte";
  import { ExperimentState } from "../../../definitions/experimentState"
  import Test from "../../common/Test.svelte"
  import DetailView from "../../common/DetailView.svelte"
  import ComparisonView from "../../common/ComparisonView.svelte"
  import { onMount } from "svelte"


  // let selectedRows: Record<string, boolean> = {};
  // let currentView = 'table'; 
  // let selectedRowId;
  // let selectedRowIds = [];

  // let tasks: Task[] = []
  let errorData: ModalData = undefined

  let infoBoxContent = "<ul><li><p>View a comprehensive record of your past experiments for a selected network, with a table of tasks and performance metrics. Click on any row to explore the experiment in detail using visualizations and learned representations.</p><p>The Reports page empowers you to iteratively improve your models and approaches based on past results, ultimately fostering a better understanding and application of graph learning techniques.</p></li></ul>";
  $: isInfoModalOpen = false

  let tasks: Task[] = [];
  let selectedRows: Record<string, boolean> = {};  
  let currentView = 'table'; 
  let selectedRowId: string;  
  let selectedRowIds: string[] = [];  

  onMount(async () => {
    updateTasks();
  });

  // when the selected network changes, update the tasks
  $: {
    console.log($selectedNetworkIndex + " is this")
    updateTasks()
  }


  async function updateTasks() {
    await getExperimentTasks($networksList[$selectedNetworkIndex].metadata.id)
      .then((incomingTasks) => {
        tasks = incomingTasks
        // @ts-ignore
        tasks = tasks.filter((task) => ExperimentState[task.state] === ExperimentState.RESULT)
        for (var i = 0; i < tasks.length; i++) {
          // @ts-ignore
          tasks[i].index = i
        }
        console.log("Reports page, updateTasks function, tasks: ", tasks)
      })
      .catch((error) => {
        errorData = new ModalData(
          null,
          `Error retrieving tasks for ${$networksList[$selectedNetworkIndex].metadata.name}}`,
          error.message,
          true
        )
        console.log(error)
      })
  }


  function selectRow(taskId: string, event) {  
    if(event.target.checked) {
      selectedRowIds = [...selectedRowIds, taskId];
    } else {
      selectedRowIds = selectedRowIds.filter(id => id !== taskId);
    }
    selectedRows = { ...selectedRows, [taskId]: event.target.checked };
  }

  function showRow(taskId: string) {  
    selectedRowId = taskId;
    currentView = 'detail'; 
  }

  function compareRows() {
    currentView = 'compare'; 
  }

  function backToTable() {
    currentView = 'table';
  }
</script>

<div
  in:fly={{ y: -50, duration: 250, delay: 300 }}
  out:fly={{ y: -50, duration: 250 }}

>

{#if currentView === 'table'}
  <!-- Table View -->
  <table>
    <thead>
      <tr>
        <th></th>
        <th>ID</th>
        <th>Task Type</th>
        <th>ML Model</th>
        <th>Epochs</th>
        <th>Train Percentage</th>
        <th>Created At</th>
      </tr>
    </thead>
    <tbody>
      {#each tasks as task (task.id)}
  <tr on:click={() => showRow(task.id)}>
    <td><input type="checkbox" bind:checked={selectedRows[task.id]} on:click|stopPropagation={(e) => selectRow(task.id, e)} /></td>
    <td>{'Experiment ' + task.id}</td>
    <td>{task.taskType}</td>
    <td>{task.mlModelType}</td>
    <td>{task.epochs}</td>
    <td>{task.trainPercentage}</td>
    <td>{task.createdAt.toDate().toLocaleString()}</td>
  </tr>
{/each}
    </tbody>
  </table>

  <button on:click={compareRows}>Compare</button>

  <p>Selected Rows:</p>
<ul>
  {#each selectedRowIds as taskId}
  <li>{'Experiment ' + taskId}</li>
{/each}
</ul>

{:else if currentView === 'detail'}
  <!-- Detail View -->
  <DetailView {selectedRowId} on:back={backToTable} />
{:else if currentView === 'compare'}
  <!-- Comparison View -->
  <ComparisonView {selectedRowIds} on:back={backToTable} />
{/if}

  
</div>

<div class="info">
  <InfoBox
    bind:isInfoModalOpen
    headerText="My Networks Guide"
    bodyText={infoBoxContent}
  />
</div>

<style lang="scss">
  .reports {
    margin-left: 10%;
    margin-right: 10%;
  }
</style>
