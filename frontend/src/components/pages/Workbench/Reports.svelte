<script lang="ts">
  import { DataTable } from "carbon-components-svelte";
  import DropdownSelector from "../../common/DropdownSelector.svelte";
  import { dropdownSelectorType } from "../../../definitions/dropdownSelectorType";
  import { selectedNetworkIndex, networksList } from "../../../stores";
  import { getExperimentTasks } from "../../../api/firebase";
  import type { Task } from "../../../definitions/task";
  import { ModalData } from "../../../definitions/modalData";
  import { onMount } from "svelte";
  import { fade, slide, scale, fly } from "svelte/transition";

  let tasks: Task[] = [];
  let errorData: ModalData = undefined;

  // onMount(() => updateTasks());

  $: {
    console.log($selectedNetworkIndex + " is this");
    updateTasks();
  }

  async function updateTasks() {
    await getExperimentTasks($networksList[$selectedNetworkIndex].metadata.id)
      .then((incomingTasks) => {
        tasks = incomingTasks;
        for (var i = 0; i < tasks.length; i++) {
          tasks[i].index = i;
        }
        console.log("Reports page, updateTasks function, tasks: ", tasks);
      })
      .catch((error) => {
        errorData = new ModalData(
          null,
          `Error retrieving tasks for ${$networksList[$selectedNetworkIndex].metadata.name}}`,
          error.message,
          true
        );
        console.log(error);
      });
  }
</script>

<div
  in:fly={{ y: -50, duration: 250, delay: 300 }}
  out:fly={{ y: -50, duration: 250 }}
>
  <DropdownSelector
    placeholder={"Select a Network"}
    type={dropdownSelectorType.NETWORK}
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
          id: task.index,
          name: "Experiment " + (task.index + 1),
          taskType: task.taskType,
          mlModelType: task.mlModelType,
          epochs: task.epochs,
          trainPercentage: task.trainPercentage,
        }))}
      >
        <svelte:fragment slot="expanded-row" let:row>
          <pre>{JSON.stringify(row, null, 2)}</pre>
        </svelte:fragment>
      </DataTable>
    {/if}
  </div>
</div>

<style lang="scss">
  .reports {
    margin-left: 10%;
    margin-right: 10%;
  }
</style>
