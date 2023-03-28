import type { View } from "vega"

export class ExperimentPlots{
    constructor(
        public lossPlot: View = undefined,
        public predictionPlot: View = undefined,
    ){}
}