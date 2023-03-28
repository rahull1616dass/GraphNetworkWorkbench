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

  let experimentPlots = {
    "plotLoss": undefined,
    "plotNodeEmbeddding": undefined,
    "plotPrediction": undefined,
  }

  async function downloadPDF() {
    const cardsPerPage: number = 1
    const imageScalingFactor: number = 0.2
    const pdf: jsPDF = new jsPDF({ format: "a4", orientation: "p" })

    const cardElements: NodeListOf<Element> = document.querySelectorAll(".container > *")

    for (let i = 0; i < cardElements.length; i++) {
      const cardElement = cardElements[i] as HTMLElement

      if (cardElement.querySelector(".vega-embed")) {
        // If the card contains a Vega-Embed chart
        const vegaView = experimentPlots[cardElement.id] as View
        if (vegaView) {
          try {
            const imgURL = await vegaView.toImageURL("png")
            const img = new Image()
            img.src = imgURL
            await new Promise((resolve) => (img.onload = resolve))

            const page = Math.floor(i / cardsPerPage)
            const xOffset = 50 //i % 2 === 0 ? 50 : 50 + img.width / 2
            const yOffset = 50//100 + (img.height + 50) * (i % cardsPerPage)

            if (page > 0 && i % cardsPerPage === 0) {
              pdf.addPage("a4", "p")
            }

            pdf.addImage({
              imageData: img,
              format: "PNG",
              x: xOffset,
              y: yOffset,
              width: img.width * imageScalingFactor,
              height: img.height * imageScalingFactor,
            })
          } catch (error) {
            console.error("Error exporting Vega chart:", error)
          }
        }
      } else {
        // If the card does not contain a Vega-Embed chart
        const canvas = await html2canvas(cardElement)
        const imgData = canvas.toDataURL("image/png")

        const page = Math.floor(i / cardsPerPage)
        const xOffset = 50 // i % 2 === 0 ? 50 : 50 + canvas.width / 2
        const yOffset = 50 //100 + (canvas.height + 50) * (i % cardsPerPage)

        if (page > 0 && i % cardsPerPage === 0) {
          pdf.addPage("a4", "p")
        }

        pdf.addImage({
          imageData: imgData,
          format: "PNG",
          x: xOffset,
          y: yOffset,
          width: canvas.width * imageScalingFactor,
          height: canvas.height * imageScalingFactor,
        })
      }
    }

    pdf.save("results.pdf")
  }
</script>

<div class="container">
  <CardView>
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

  <CardView id="plotLoss">
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

  <CardView id="plotNodeEmbedding">
    <h4 slot="header">Node Embedding</h4>
    <div slot="body">
      <Embedding on:plotLoaded={(e) => {
        experimentPlots["plotNodeEmbedding"] = e.detail
      }}/>
    </div>

    <div slot="footer" />
  </CardView>

  <CardView id="plotPrediction">
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
