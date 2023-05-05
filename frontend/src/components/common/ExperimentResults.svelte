<script lang="ts">
  import CardView from "./CardView.svelte"
  import Embedding from "./Embedding.svelte"
  import PlotLoss from "./PlotLoss.svelte"
  import PlotPrediction from "./PlotPrediction.svelte"
  import type { Task } from "../../definitions/task"
  import type { Network } from "../../definitions/network"
  import type { View } from "vega"
  import { ExperimentPlots } from "../../definitions/experimentPlots"
  import CustomButton from "./CustomButton.svelte"
  import html2canvas from "html2canvas"
  import jsPDF from "jspdf"
  import { fade } from "svelte/transition";

  export let task: Task = undefined
  export let currentNetwork: Network = undefined
  

  let nodeDataResult
  let edgeDataResult

  let experimentPlots = {
    plotLoss: undefined,
    plotNodeEmbeddding: undefined,
    plotPrediction: undefined,
  }

  let showDetails = false;

function toggleDetails() {
  showDetails = !showDetails;
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

          const availableWidth = pdf.internal.pageSize.getWidth() - 2 * xOffset;
          const widthScalingFactor = availableWidth / img.width;
          const imageScalingFactor = widthScalingFactor;

          const page = Math.floor(i / cardsPerPage);
          const yOffset = 50 + (img.height * imageScalingFactor + 50) * (i % cardsPerPage);

          if (page > 0 && i % cardsPerPage === 0) {
            pdf.addPage("a4", "p");
          }
          pdf.text(
            title,
            pdf.internal.pageSize.getWidth() / 2,
            30,
            { align: "center" }
          );
          pdf.addImage({
            imageData: img,
            format: "PNG",
            x: xOffset,
            y: yOffset,
            width: img.width * imageScalingFactor,
            height: img.height * imageScalingFactor,
          });
          
          if(title === "Prediction Results"){
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
      const yOffset = 50 + (canvas.height * imageScalingFactor + 50) * (i % cardsPerPage);

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
  let result:string = node.result == 1?"In Training":node.result == 2?"Correct":node.result ==3?"Wrong":"Not Defined"
  return `name: ${node.name}, index: ${node.index}, result: ${result}`;
}

function formatEdgeData(edge) {
  let result:string = edge.result == 1?"In Training":edge.result == 2?"Correct":edge.result ==3?"Wrong":"Not Defined"
  return `source: ${edge.source}, target: ${edge.target}, result: ${result}`;
}

async function addNodeData(pdf: jsPDF) {
    const yOffsetStart = 50;
    const yOffsetIncrement = 20;
    const xOffsetNodeData = 50;
    let yOffsetNodeData = yOffsetStart;

    if(nodeDataResult !== undefined){
          pdf.addPage("a4", "p");
          pdf.text("Node Results", pdf.internal.pageSize.getWidth() / 2, yOffsetNodeData, { align: "center" });
          yOffsetNodeData += yOffsetIncrement;

          nodeDataResult.forEach((node) => {
            pdf.text(formatNodeData(node), xOffsetNodeData, yOffsetNodeData);
            yOffsetNodeData += yOffsetIncrement;

            // Check if yOffsetNodeData exceeds the page height, and if so, add a new page and reset yOffsetNodeData
            if (yOffsetNodeData >= pdf.internal.pageSize.getHeight() - yOffsetStart) {
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
    if(edgeDataResult!== undefined){
    pdf.addPage("a4", "p");
    pdf.text("Edge Results", pdf.internal.pageSize.getWidth() / 2, yOffsetEdgeData, { align: "center" });
    yOffsetEdgeData += yOffsetIncrement;
   
      edgeDataResult.forEach((edge) => {
        pdf.text(formatEdgeData(edge), xOffsetEdgeData, yOffsetEdgeData);
        yOffsetEdgeData += yOffsetIncrement;

        // Check if yOffsetEdgeData exceeds the page height, and if so, add a new page and reset yOffsetEdgeData
        if (yOffsetEdgeData >= pdf.internal.pageSize.getHeight() - yOffsetStart) {
          pdf.addPage("a4", "p");
          yOffsetEdgeData = yOffsetStart;
        }
      });
    }
  }
</script>

<div class="circle-container">
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="circle" on:click={() => (showDetails = !showDetails)}>
    <div class="accuracy">
      {task.accuracy}%
    </div>
    {#if showDetails}
      <div class="details">
        <p>F1 score:{task.f1}</p>
        <p>Precision:{task.precision}</p>
        <p>Recall:{task.recall}</p>
        <p>AUC:{task.auc}</p>
      </div>
    {/if}
  </div>
</div>

<div class="download_results">
  <CustomButton
    type={"secondary"}
    inverse={false}
    fontsize={60}
    on:click={() => downloadPDF()}>Download Results as PDF</CustomButton
  >
</div>

<style>
  .circle-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
}

.circle {
  width: 200px;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: rgba(75, 192, 192, 0.5);
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 1000;
  overflow: hidden;
}

.accuracy {
  font-size: 1.5rem;
  transition: font-size 0.3s ease, margin-top 0.3s ease;
}

.circle:hover .accuracy {
  font-size: 2rem;
  margin-top: -10px;
}

.details {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 0.9rem;
  opacity: 0;
  transition: opacity 0.5s ease;
}

.circle:hover .details {
  opacity: 1;
}



.details p {
  margin-bottom: 0;
}


  p {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
      Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
      sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
  }
</style>
