<script lang="ts">
  import { DataTable } from "carbon-components-svelte";
  import DropdownSelector from "../../common/DropdownSelector.svelte";
  import { DropdownSelectorType } from "../../../definitions/dropdownSelectorType";
  import { selectedNetworkIndex, networksList } from "../../../stores";
  import { getExperimentTasks } from "../../../api/firebase";
  import type { Task } from "../../../definitions/task";
  import { ModalData } from "../../../definitions/modalData";
  import { onMount } from "svelte";
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
          // @ts-ignore
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
        <pre>{JSON.stringify(row, null, 2)}</pre>
      </svelte:fragment>
    </DataTable>
  {/if}
</div>

<style lang="scss">
  .reports {
    margin-left: 10%;
    margin-right: 10%;
  }
</style>
