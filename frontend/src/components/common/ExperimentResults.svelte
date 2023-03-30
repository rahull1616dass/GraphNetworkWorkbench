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

  export let task: Task = undefined
  export let currentNetwork: Network = undefined

  let nodeDataResult
  let edgeDataResult

  let experimentPlots = {
    plotLoss: undefined,
    plotNodeEmbeddding: undefined,
    plotPrediction: undefined,
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
  return `source: ${edge.source}, target: ${edge.target}, result: ${edge.result}`;
}

async function addNodeData(pdf: jsPDF) {
    const yOffsetStart = 50;
    const yOffsetIncrement = 20;
    const xOffsetNodeData = 50;
    let yOffsetNodeData = yOffsetStart;

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

  async function addEdgeData(pdf: jsPDF) {
    const yOffsetStart = 50;
    const yOffsetIncrement = 20;
    const xOffsetEdgeData = 50;
    let yOffsetEdgeData = yOffsetStart;

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
</script>

<div class="container">
  <CardView title="Metrics">
    <h4 slot="header">Details</h4>
    <div slot="body">
      <p>Accuracy:{task.accuracy}</p>
      <p>F1 score:{task.f1}</p>
      <p>Precision:{task.precision}</p>
      <p>Recall:{task.recall}</p>
      <p>AUC:{task.auc}</p>
    </div>

    <div slot="footer" />
  </CardView>

  <CardView id="plotLoss" title="Loss Function">
    <h4 slot="header">Loss Function</h4>
    <div slot="body">
      <PlotLoss
        losses={task.losses}
        on:plotLoaded={(e) => {
          experimentPlots["plotLoss"] = e.detail
        }}
      />
    </div>
    <div slot="footer" />
  </CardView>

  <CardView id="plotNodeEmbedding" title="Node Embeddings">
    <h4 slot="header">Node Embedding</h4>
    <div slot="body">
      <Embedding
        on:plotLoaded={(e) => {
          experimentPlots["plotNodeEmbedding"] = e.detail
        }}
      />
    </div>

    <div slot="footer" />
  </CardView>

  <CardView id="plotPrediction" title="Prediction Results">
    <h4 slot="header">Network Results</h4>
    <div slot="body">
      <p>
        Green nodes/edges for correct predictions, red nodes/edges for false
        predictions
      </p>
      <PlotPrediction
        {task}
        {currentNetwork}
        on:predictionPlotLoaded={(e) => {
          experimentPlots["plotPrediction"] = e.detail
        }}
        on:nodeData={(e) => {
          nodeDataResult = e.detail
        }}
        on:edgeData={(e) => {
          edgeDataResult = e.detail
        }}

      />
    </div>

    <div slot="footer" />
  </CardView>

  <CardView>
    <h4 slot="header">Expert Opinion</h4>
    <div slot="body">
      <p>{task.expertOpinion}</p>
    </div>
    <div slot="footer" />
  </CardView>
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
  .container {
    display: grid;
    grid-template-rows: repeat(3, 1fr);
    grid-template-columns: repeat(2, 1fr);
    gap: 2%;
    margin: 2%;
  }
  p {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
      Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
      sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
  }
</style>
