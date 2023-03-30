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

  let tasks: Task[] = []
  let errorData: ModalData = undefined

  let infoBoxContent = "<ul><li><p>View a comprehensive record of your past experiments for a selected network, with a table of tasks and performance metrics. Click on any row to explore the experiment in detail using visualizations and learned representations.</p><p>The Reports page empowers you to iteratively improve your models and approaches based on past results, ultimately fostering a better understanding and application of graph learning techniques.</p></li></ul>";
  $: isInfoModalOpen = false

  // onMount(() => updateTasks());

  $: {
    console.log($selectedNetworkIndex + " is this")
    updateTasks()
  }

  async function updateTasks() {
    await getExperimentTasks($networksList[$selectedNetworkIndex].metadata.id)
      .then((incomingTasks) => {
        tasks = incomingTasks
        // @ts-ignore
        tasks = tasks.filter((task) => ExperimentState[task.state] !== ExperimentState.PROGRESS)
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
</script>

<div
  in:fly={{ y: -50, duration: 250, delay: 300 }}
  out:fly={{ y: -50, duration: 250 }}
>
  <DropdownSelector
    placeholder={"Select a Network"}
    type={DropdownSelectorType.NETWORK}
  />
  <div class="reports">
    {#if errorData !== undefined}
      <h2>{errorData.messageHeader}</h2>
      <p>{errorData.messageBody}</p>
    {:else}
      <DataTable
        zebra
        expandable
        stickyHeader
        sortable
        headers={[
          { key: "name", value: "ID" },
          { key: "taskType", value: "Task Type" },
          { key: "mlModelType", value: "ML Model" },
          { key: "epochs", value: "Epochs" },
          { key: "trainPercentage", value: "Train Percentage" },
        ]}
        rows={tasks.map((task) => ({
          // @ts-ignore
          id: task.index,
          // @ts-ignore
          name: "Experiment " + (task.index + 1),
          taskType: task.taskType,
          mlModelType: task.mlModelType,
          epochs: task.epochs,
          trainPercentage: task.trainPercentage,
        }))}
      >
        <svelte:fragment slot="expanded-row" let:row>
            <ExperimentResults task={tasks[row.id]} currentNetwork={$networksList[$selectedNetworkIndex]} />
        </svelte:fragment>
      </DataTable>
    {/if}
  </div>

  
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
