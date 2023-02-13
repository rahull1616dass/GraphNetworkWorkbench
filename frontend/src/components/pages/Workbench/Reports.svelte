<script lang="ts">
  import { DataTable } from "carbon-components-svelte";
  import DropdownSelector from "../../common/DropdownSelector.svelte";
  import { dropdownSelectorType } from "../../../definitions/dropdownSelectorType";
  import { selectedNetworkIndex, networksList } from "../../../stores";
  import { getExperimentTasks } from "../../../api/firebase";
  import type { Task } from "../../../definitions/task";
  import { ModalData } from "../../../definitions/modalData";
  import { onMount } from "svelte";
  let tasks: Task[] = [];
  let errorData: ModalData = undefined;

  onMount(() => updateTasks());

  // $: {
  //   console.log($selectedNetworkIndex + " is this")
  //   updateTasks()
  // }

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

<DropdownSelector
  placeholder={"Select a Network"}
  type={dropdownSelectorType.NETWORK}
/>

{#if errorData !== undefined}
  <h2>{errorData.messageHeader}</h2>
  <p>{errorData.messageBody}</p>
{:else}
  hello
  <DataTable
    zebra
    expandable
    headers={[
      { key: "id", value: "ID" },
      { key: "taskType", value: "Task Type" },
      { key: "mlModelType", value: "ML Model" },
      { key: "epochs", value: "Epochs" },
      { key: "trainPercentage", value: "Train Percentage" },
    ]}
    rows={tasks.map((task) => ({
      id: task.index,
      taskType: task.taskType,
      mlModelType: task.mlModelType,
      epochs: task.epochs,
      trainPercentage: task.trainPercentage,
    }))}
  />
{/if}

<style lang="scss">
</style>
