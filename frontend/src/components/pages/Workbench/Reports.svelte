<script lang="ts">
  import { DataTable } from "carbon-components-svelte"
  import DropdownSelector from "../../common/DropdownSelector.svelte"
  import { selectedNetworkIndex, networksList } from "../../../stores"
  import { getExperimentTasks } from "../../../api/firebase"
  import type { Task } from "../../../definitions/task"
  import { ModalData } from "../../../definitions/modalData"
  import { onMount } from "svelte"
  let tasks: Task[] = []
  let errorData: ModalData = undefined

  //onMount(() => updateTasks())

  $: {
    console.log($selectedNetworkIndex + " is this")
    updateTasks()
  }

  function updateTasks() {
    getExperimentTasks($networksList[$selectedNetworkIndex].metadata.id)
      .then((incomingTasks) => {
        tasks = incomingTasks
        console.log(tasks)
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

<DropdownSelector />

{#if errorData !== undefined}
  <h2>{errorData.messageHeader}</h2>
  <p>{errorData.messageBody}</p>
{:else}
  <DataTable
    expandable
    headers={[
      { key: "id", value: "ID" },
      { key: "taskType", value: "Task Type" },
      { key: "epochs", value: "Epochs" },
      { key: "trainPercentage", value: "Train Percentage" },
    ]}
    rows={tasks.map((task) => ({
      id: task.id,
      taskType: task.taskType,
      epochs: task.epochs,
      trainPercentage: task.trainPercentage,
    }))}
  />
{/if}

<style lang="scss">
</style>
