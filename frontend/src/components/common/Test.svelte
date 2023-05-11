<script lang="ts">
    
    import DetailView from './DetailView.svelte'; 
    import ComparisonView from './ComparisonView.svelte';


let rows = [
  { id: 1, name: "John", age: 30 },
  { id: 2, name: "Doe", age: 25 },
  { id: 3, name: "Marry", age: 28 },
  { id: 4, name: "Smith", age: 35 },
];

let selectedRows: Record<string, boolean> = {};
  let currentView = 'table'; 
  let selectedRowId;
  let selectedRowIds = []; // array to keep track of selected row ids

  function selectRow(rowId, event) {
    if(event.target.checked) {
      selectedRowIds = [...selectedRowIds, rowId];
    } else {
      selectedRowIds = selectedRowIds.filter(id => id !== rowId);
    }
    selectedRows = { ...selectedRows, [rowId]: event.target.checked };
  }

  function showRow(rowId) {
    selectedRowId = rowId;
    currentView = 'detail'; 
  }

  function compareRows() {
    currentView = 'compare'; // switch to the comparison view
  }

  function backToTable() {
    currentView = 'table';
  }
  </script>

{#if currentView === 'table'}

<button on:click={compareRows}>Compare</button>
  
  <table>
    <thead>
      <tr>
        <th>Select</th>
        <th>ID</th>
        <th>Name</th>
        <th>Age</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {#each rows as row}
        <tr>
            <input type="checkbox" bind:checked={selectedRows[row.id]} on:change={(e) => selectRow(row.id, e)}>

          <td>{row.id}</td>
          <td>{row.name}</td>
          <td>{row.age}</td>
          <td><button on:click={() => showRow(row.id)}>Show</button></td>
        </tr>
      {/each}
    </tbody>
  </table>
  
  <p>Selected Rows:</p>
  <ul>
    {#each Object.keys(selectedRows).filter(id => selectedRows[id]) as rowId}
      <li>{rows.find(row => row.id === Number(rowId)).name}</li>
    {/each}
  </ul>

  {:else if currentView === 'detail'}
  <!-- Detail View -->
  <DetailView {selectedRowId} on:back={backToTable} />
{:else if currentView === 'compare'}
  <!-- Comparison View -->
  <ComparisonView {selectedRowIds} on:back={backToTable} />
{/if}
  
  
  <style>
    table {
      border-collapse: collapse;
      width: 100%;
    }
    th, td {
      border: 1px solid black;
      padding: 8px;
      text-align: left;
    }
  </style>
  