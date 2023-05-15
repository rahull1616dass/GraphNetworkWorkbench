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

  $: selectedTask = tasks.find(task => task.id === selectedRowId);



  async function updateTasks() {
    await getExperimentTasks($networksList[$selectedNetworkIndex].metadata.id)
      .then((incomingTasks) => {
        tasks = incomingTasks
        // @ts-ignore
        tasks = tasks.filter((task) => ExperimentState[task.state] !== ExperimentState.CREATE)
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

<DropdownSelector
    placeholder={"Select a Network"}
    type={DropdownSelectorType.NETWORK}
  />


  <!-- Table View -->
  <dıv class='report_container'>


  <table>
    <thead>
      <tr>
        <th></th>
        <th>ID</th>
        <th>Status</th>
        <th>Task Type</th>
        <th>ML Model</th>
        <th>Epochs</th>
        <th>Train Percentage</th>
        <th>Accuracy</th>
        <th>Created At</th>
      </tr>
    </thead>
    <tbody>
      {#each tasks as task (task.id)}
  <tr on:click={() => showRow(task.id)}>
    <td><input type="checkbox" bind:checked={selectedRows[task.id]} on:click|stopPropagation={(e) => selectRow(task.id, e)} /></td>
    <td>{'Experiment ' + task.id}</td>
    <td>
      {#if task.state === ExperimentState.RESULT}
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52" width="20" height="20">
        <circle style="fill:#4CAF50;" cx="26" cy="26" r="26"/>
        <polyline style="fill:none;stroke:#FFFFFF;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:10;" points="38,15 22,33 15,25"/>
      </svg>

      {:else if task.state === ExperimentState.ERROR}
      
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52" width="20" height="20">
        <circle style="fill:#F44336;" cx="26" cy="26" r="26"/>
        <line x1="16" y1="16" x2="36" y2="36" style="stroke:#FFFFFF;stroke-width:2"/>
        <line x1="36" y1="16" x2="16" y2="36" style="stroke:#FFFFFF;stroke-width:2"/>
      </svg>

      {:else if task.state === ExperimentState.PROGRESS}
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52" width="20" height="20">
        <circle style="fill:transparent; stroke:#FFA500; stroke-width:5" cx="26" cy="26" r="23"/>
      </svg>
      
      
      {/if}
      <!-- {task.state} -->
      
    </td>
    <td>{task.taskType}</td>
    <td>{task.mlModelType}</td>
    <td>{task.epochs}</td>
    <td>{task.trainPercentage}</td>
    <td>{task.accuracy}</td>
    <td>{task.createdAt.toDate().toLocaleString()}</td>
  </tr>
{/each}
    </tbody>
  </table>
</dıv>

  <button on:click={compareRows}>Compare</button>

{:else if currentView === 'detail'}

  <!-- Detail View -->
  <DetailView task={selectedTask} {selectedNetworkIndex} on:back={backToTable} />

{:else if currentView === 'compare'}
  <!-- Comparison View -->
  <!-- {selectedTask.id} -->

  <ComparisonView {selectedRowIds} {tasks} currentNetwork={$networksList[$selectedNetworkIndex]} on:back={backToTable} />
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

svg {
  width: 20px;
  height: 20px;
}


.report_container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  padding: 20px;
  box-sizing: border-box;
  background-color: #f0f0f0; /* Light gray background for contrast */
  border-radius: 10px; /* Rounded corners */
  box-shadow: 0px 0px 10px rgba(0,0,0,0.1); /* Slight shadow for a lifted effect */
  max-height: 50%;
  overflow: auto;
}

    table {
    border-collapse: collapse;
    width: 100%;
  }

  th,
  td {
    text-align: left;
    padding: 8px;
  }

  th {
    background-color: #f2f2f2;
    font-weight: bold;
  }

  tr:nth-child(even) {
    background-color: whitesmoke;
  }
  .reports {
    margin-left: 10%;
    margin-right: 10%;
  }
</style>
