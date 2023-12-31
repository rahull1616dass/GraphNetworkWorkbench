<script lang="ts">
  import CardView from "./CardView.svelte";
  import Embedding from "./Embedding.svelte";
  import PlotLoss from "./PlotLoss.svelte";
  import PlotPrediction from "./PlotPrediction.svelte";
  import type { Task } from "../../definitions/task";
  import type { Network } from "../../definitions/network";
  import type { View } from "vega";
  import { ExperimentPlots } from "../../definitions/experimentPlots";
  import CustomButton from "./CustomButton.svelte";
  import html2canvas from "html2canvas";
  import jsPDF from "jspdf";
  import { fade } from "svelte/transition";
  import CustomModal from "./CustomModal.svelte";
  import { createEventDispatcher } from "svelte";
  import CustomDataTable from "./CustomDataTable.svelte";
  import { networksList, selectedNetworkIndex } from "../../stores";

  export let task: Task = undefined;
  export let forReport = false;
  const dispatch = createEventDispatcher();
  let currentNetwork = $networksList[$selectedNetworkIndex];

  let showExplanation = false;

  let nodeDataResult;
  let edgeDataResult;

  let experimentPlots = {
    plotLoss: undefined,
    plotNodeEmbeddding: undefined,
    plotPrediction: undefined,
  };

  let showDetails = false;
  let showRunDetails = false;
  // $: buttonText = showDetails ? "Hide Run Details" : "Show Run Details";

  function toggleDetails() {
    showDetails = !showDetails;
  }

  let modalState = { isOpen: false, circleName: "", description: "" };

  function openModal(circleName) {
    modalState.isOpen = true;
    modalState.circleName = circleName;
    if (circleName === "Accuracy") {
      modalState.description =
        "Accuracy is a metric used to evaluate the performance of classification models. It measures the proportion of correct predictions made by the model out of the total number of predictions. In simple terms, it represents how well a model correctly classifies the given data.";
    } else if (circleName === "Precision") {
      modalState.description =
        "Precision is a metric used to evaluate the performance of classification models. It is the proportion of true positives that are correctly identified. It is a better metric than accuracy when the dataset is imbalanced.";
    } else if (circleName === "F1 Score") {
      modalState.description =
        "F1 Score is a metric used to evaluate the performance of classification models. It is the harmonic mean of precision and recall. It is a better metric than accuracy when the dataset is imbalanced.";
    } else if (circleName === "AUC Score") {
      modalState.description =
        "AUC Score is a metric used to evaluate the performance of classification models. It is the area under the ROC curve. It is a better metric than accuracy when the dataset is imbalanced.";
    } else if (circleName == "Recall") {
      modalState.description =
        "Recall is a metric used to evaluate the performance of classification models. It is the proportion of true positives that are correctly identified. It is a better metric than accuracy when the dataset is imbalanced.";
    } else {
      modalState.description = "Not defined";
    }
  }

  function closeModal() {
    modalState.isOpen = false;
    modalState.circleName = "";
  }

  let backgroundColor;
  $: {
    if (task.accuracy >= 0.8) {
      backgroundColor = "#2cba00";
    } else if (task.accuracy >= 0.6) {
      backgroundColor = "#92E500";
    } else if (task.accuracy >= 0.4) {
      backgroundColor = "#E5DB00";
    } else if (task.accuracy >= 0.2) {
      backgroundColor = "#ffa700";
    } else {
      backgroundColor = "#ff0000";
    }
  }

  let fontSize = {
    accuracy: 16,
    f1Score: 16,
    precision: 16,
    recall: 16,
    auc: 16,
  };

  function changeFontSize(id, isMouseOver) {
    fontSize[id] = isMouseOver ? 22 : 16;
  }

  async function downloadPDF() {
    const cardsPerPage: number = 1;
    const xOffset = 50;
    const pdf: jsPDF = new jsPDF({ format: "a4", orientation: "p" });
    pdf.setFontSize(20);

    const cardElements: NodeListOf<Element> =
      document.querySelectorAll(".container > *");

    for (let i = 0; i < cardElements.length; i++) {
      const cardElement = cardElements[i] as HTMLElement;

      if (cardElement.querySelector(".vega-embed")) {
        // If the card contains a Vega-Embed chart
        const vegaView = experimentPlots[cardElement.id] as View;
        const title = cardElement.getAttribute("data-title");
        if (vegaView) {
          try {
            const imgURL = await vegaView.toImageURL("png");
            const img = new Image();
            img.src = imgURL;
            await new Promise((resolve) => (img.onload = resolve));

            const availableWidth =
              pdf.internal.pageSize.getWidth() - 2 * xOffset;
            const widthScalingFactor = availableWidth / img.width;
            const imageScalingFactor = widthScalingFactor;

            const page = Math.floor(i / cardsPerPage);
            const yOffset =
              50 + (img.height * imageScalingFactor + 50) * (i % cardsPerPage);

            if (page > 0 && i % cardsPerPage === 0) {
              pdf.addPage("a4", "p");
            }
            pdf.text(title, pdf.internal.pageSize.getWidth() / 2, 30, {
              align: "center",
            });
            pdf.addImage({
              imageData: img,
              format: "PNG",
              x: xOffset,
              y: yOffset,
              width: img.width * imageScalingFactor,
              height: img.height * imageScalingFactor,
            });

            if (title === "Prediction Results") {
              await addNodeData(pdf);
              await addEdgeData(pdf);
            }
          } catch (error) {
            console.error("Error exporting Vega chart:", error);
          }
        }
      } else {
        // If the card does not contain a Vega-Embed chart
        const canvas = await html2canvas(cardElement);
        const imgData = canvas.toDataURL("image/png");

        const availableWidth = pdf.internal.pageSize.getWidth() - 2 * xOffset;
        const widthScalingFactor = availableWidth / canvas.width;
        const imageScalingFactor = widthScalingFactor * 0.5;

        const page = Math.floor(i / cardsPerPage);
        const yOffset =
          50 + (canvas.height * imageScalingFactor + 50) * (i % cardsPerPage);

        if (page > 0 && i % cardsPerPage === 0) {
          pdf.addPage("a4", "p");
        }

        pdf.addImage({
          imageData: imgData,
          format: "PNG",
          x: xOffset,
          y: yOffset,
          width: canvas.width * imageScalingFactor,
          height: canvas.height * imageScalingFactor,
        });
      }
    }

    pdf.save("results.pdf");
  }

  function formatNodeData(node) {
    let result: string =
      node.result == 1
        ? "In Training"
        : node.result == 2
        ? "Correct"
        : node.result == 3
        ? "Wrong"
        : "Not Defined";
    return `name: ${node.name}, index: ${node.index}, result: ${result}`;
  }

  function formatEdgeData(edge) {
    let result: string =
      edge.result == 1
        ? "In Training"
        : edge.result == 2
        ? "Correct"
        : edge.result == 3
        ? "Wrong"
        : "Not Defined";
    return `source: ${edge.source}, target: ${edge.target}, result: ${result}`;
  }

  async function addNodeData(pdf: jsPDF) {
    const yOffsetStart = 50;
    const yOffsetIncrement = 20;
    const xOffsetNodeData = 50;
    let yOffsetNodeData = yOffsetStart;

    if (nodeDataResult !== undefined) {
      pdf.addPage("a4", "p");
      pdf.text(
        "Node Results",
        pdf.internal.pageSize.getWidth() / 2,
        yOffsetNodeData,
        { align: "center" }
      );
      yOffsetNodeData += yOffsetIncrement;

      nodeDataResult.forEach((node) => {
        pdf.text(formatNodeData(node), xOffsetNodeData, yOffsetNodeData);
        yOffsetNodeData += yOffsetIncrement;

        // Check if yOffsetNodeData exceeds the page height, and if so, add a new page and reset yOffsetNodeData
        if (
          yOffsetNodeData >=
          pdf.internal.pageSize.getHeight() - yOffsetStart
        ) {
          pdf.addPage("a4", "p");
          yOffsetNodeData = yOffsetStart;
        }
      });
    }
  }

  async function addEdgeData(pdf: jsPDF) {
    const yOffsetStart = 50;
    const yOffsetIncrement = 20;
    const xOffsetEdgeData = 50;
    let yOffsetEdgeData = yOffsetStart;
    if (edgeDataResult !== undefined) {
      pdf.addPage("a4", "p");
      pdf.text(
        "Edge Results",
        pdf.internal.pageSize.getWidth() / 2,
        yOffsetEdgeData,
        { align: "center" }
      );
      yOffsetEdgeData += yOffsetIncrement;

      edgeDataResult.forEach((edge) => {
        pdf.text(formatEdgeData(edge), xOffsetEdgeData, yOffsetEdgeData);
        yOffsetEdgeData += yOffsetIncrement;

        // Check if yOffsetEdgeData exceeds the page height, and if so, add a new page and reset yOffsetEdgeData
        if (
          yOffsetEdgeData >=
          pdf.internal.pageSize.getHeight() - yOffsetStart
        ) {
          pdf.addPage("a4", "p");
          yOffsetEdgeData = yOffsetStart;
        }
      });
    }
  }
</script>

<div class="buttons-container">
  {#if forReport !== true}
    <div class="newExperiment">
      <CustomButton
        type={"secondary"}
        inverse={false}
        on:click={() => {
          dispatch("newExperiment");
        }}
        >New Experiment
      </CustomButton>
    </div>
  {/if}
  <div class="download_results">
    <CustomButton
      type={"secondary"}
      inverse={false}
      fontsize={120}
      on:click={() => downloadPDF()}>Download PDF</CustomButton
    >
  </div>
  <div class="show_details">
    <CustomButton
      type={"secondary"}
      inverse={false}
      fontsize={120}
      on:click={() => {
        showRunDetails = !showRunDetails;
      }}>Show/Hide Run Details</CustomButton
    >
  </div>
</div>

{#if showRunDetails === true}
  <div class="datatable">
    <CustomDataTable {currentNetwork} {task} />
  </div>
{:else}
  <div class="flex-container">
    <svg width="600" height="600">
      <!-- Lines connecting the nodes -->
      <line
        x1="300"
        y1="300"
        x2="200"
        y2="100"
        stroke="black"
        stroke-width="2"
      />
      <line
        x1="300"
        y1="300"
        x2="400"
        y2="100"
        stroke="black"
        stroke-width="2"
      />
      <line
        x1="300"
        y1="300"
        x2="150"
        y2="400"
        stroke="black"
        stroke-width="2"
      />
      <line
        x1="300"
        y1="300"
        x2="450"
        y2="400"
        stroke="black"
        stroke-width="2"
      />

      <!-- Main Node -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <circle
        cx="300"
        cy="300"
        r="80"
        fill="#03C988"
        on:mouseover={() => changeFontSize("accuracy", true)}
        on:mouseout={() => changeFontSize("accuracy", false)}
        on:click={() => openModal("Accuracy")}
      />
      <text
        class="node-text"
        x="300"
        y="290"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.accuracy}px"
        fill="white">Accuracy</text
      >
      <text
        class="node-text"
        x="300"
        y="315"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.accuracy}px"
        fill="white">{task.accuracy}</text
      >

      <!-- F1 Score Node -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <circle
        cx="200"
        cy="100"
        r="60"
        fill="#4CAF50"
        on:mouseover={() => changeFontSize("f1Score", true)}
        on:mouseout={() => changeFontSize("f1Score", false)}
        on:click={() => openModal("F1 Score")}
      />
      <text
        class="node-text"
        id="f1Score"
        x="200"
        y="90"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.f1Score}px"
        fill="white">F1 Score</text
      >
      <text
        class="node-text"
        id="f1Score"
        x="200"
        y="115"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.f1Score}px"
        fill="white">{task.f1}</text
      >

      <!-- Precision Node -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <circle
        cx="400"
        cy="100"
        r="55"
        fill="#2196F3"
        on:mouseover={() => changeFontSize("precision", true)}
        on:mouseout={() => changeFontSize("precision", false)}
        on:click={() => openModal("Precision")}
      />
      <text
        class="node-text"
        id="precision"
        x="400"
        y="90"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.precision}px"
        fill="white">Precision</text
      >
      <text
        class="node-text"
        id="precision"
        x="400"
        y="115"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.precision}px"
        fill="white">{task.precision}</text
      >

      <!-- Recall Node -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <circle
        cx="150"
        cy="400"
        r="45"
        fill="#FF9800"
        on:mouseover={() => changeFontSize("recall", true)}
        on:mouseout={() => changeFontSize("recall", false)}
        on:click={() => openModal("Recall")}
      />
      <text
        class="node-text"
        id="recall"
        x="150"
        y="390"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.recall}px"
        fill="white">Recall</text
      >
      <text
        class="node-text"
        id="recall"
        x="150"
        y="415"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.recall}px"
        fill="white">{task.recall}</text
      >

      <!-- AUC Node -->
      <!-- svelte-ignore a11y-mouse-events-have-key-events -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <circle
        cx="450"
        cy="400"
        r="70"
        fill="#9C27B0"
        on:mouseover={() => changeFontSize("auc", true)}
        on:mouseout={() => changeFontSize("auc", false)}
        on:click={() => openModal("AUC Score")}
      />
      <text
        class="node-text"
        id="auc"
        x="450"
        y="390"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.auc}px"
        fill="white">AUC</text
      >
      <text
        class="node-text"
        id="auc"
        x="450"
        y="415"
        text-anchor="middle"
        dy=".3em"
        font-size="{fontSize.auc}px"
        fill="white">{task.auc}</text
      >
    </svg>

    {#if modalState.isOpen}
      <CustomModal on:close={closeModal}>
        <h4 slot="header">
          {modalState.circleName}
        </h4>
        <div slot="body">
          {modalState.description}
        </div>

        <div slot="footer">
          <CustomButton
            type={"secondary"}
            inverse={false}
            on:click={() => {
              closeModal();
            }}
          >
            Got it!
          </CustomButton>
        </div>
      </CustomModal>
    {/if}

    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div
      class="expandable-text"
      on:click={() => (showExplanation = !showExplanation)}
    >
      <p class="question">Do you want to improve your accuracy?</p>
      {#if showExplanation}
        <div class="explanation">
          <p>
            {task.expertOpinion}
          </p>
        </div>
      {/if}
    </div>
  </div>

  <hr />

  <div class="plots-container">
    <div class="plot-wrapper">
      <h4>Loss Function</h4>
      <div>
        <PlotLoss
          losses={task.losses}
          on:plotLoaded={(e) => {
            experimentPlots["plotLoss"] = e.detail;
          }}
        />
      </div>
    </div>

    <div class="plot-wrapper">
      <h4>Node Embedding</h4>
      <div>
        <Embedding
          {task}
          on:plotLoaded={(e) => {
            experimentPlots["plotNodeEmbedding"] = e.detail;
          }}
        />
      </div>
    </div>
  </div>

  <hr />

  <h4>Network Results</h4>
  <div>
    <p>
      Green nodes/edges for correct predictions, red nodes/edges for false
      predictions
    </p>
    <PlotPrediction
      {task}
      on:predictionPlotLoaded={(e) => {
        experimentPlots["plotPrediction"] = e.detail;
      }}
      on:nodeData={(e) => {
        nodeDataResult = e.detail;
      }}
      on:edgeData={(e) => {
        edgeDataResult = e.detail;
      }}
    />
  </div>

  <div />
{/if}

<style>
  .datatable {
    margin-top: 10%;
    margin-left: 10%;
    margin-right: 10%;
  }
  .plots-container {
    display: flex;
    justify-content: space-around;
    width: 100%;
  }

  .plot-wrapper {
    width: 100%; /* Adjust this value to change the size of the plots */
    margin-right: -20px;
  }

  .node-text {
    transition: font-size 0.3s ease-in-out;
  }

  svg {
    display: block;
    margin-left: 2%;
  }

  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  .flex-container {
    display: flex;
    align-items: center;
    justify-content: space-around;
    animation: fadeIn 1s ease-in-out;
  }

  .expandable-text {
    cursor: pointer;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
      Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
      sans-serif;
    font-size: 16px;
    width: 30%;
    margin-bottom: 15%;
  }
  .question {
    color: var(--wueblue);
    font-weight: bold;
    font-size: large;
    font-style: italic;
    margin-right: 35%;
    margin-top: 2%;
  }
  .explanation {
    margin-top: 10px;
    padding: 10px;
    border-radius: 5px;
    background-color: #f9f9f9;
    margin-right: 10%;
    box-shadow: 1px 2px 3px rgba(0, 0, 0, 0.2);
    color: var(--lightblack);
    animation: fadeIn 1s ease-in-out;
  }
  .explanation p {
    margin-top: 0;
  }

  .buttons-container {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    width: 100%;
    max-width: 20%; /* Adjust this value according to your desired buttons' spacing */
    margin: 0 auto;
    margin-top: 1%;
  }

  .newExperiment {
    flex: 1;
    margin: 0 1px;
  }

  .download_results {
    flex: 1;
    margin: 0 1px;
  }

  p {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
      Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
      sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
  }
</style>
