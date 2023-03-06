import type { MLModelType } from "./mlModelType";
import type { TaskType } from "./taskType";
import type { Timestamp } from "firebase/firestore"
import type { ExperimentState } from "./experimentState"

export class Task {
  constructor(
    public id: string = undefined,
    public mlModelType: MLModelType = undefined,
    public taskType: TaskType = undefined,
    public epochs: number = undefined,
    public trainPercentage: number = undefined,
    public learningRate: number = undefined,
    public hiddenLayerSizes: number[] = undefined,
    public seed: number = undefined,
    public createdAt: Timestamp = undefined,
    public state: ExperimentState = undefined,
    public xColumns: string[] = undefined,
    public yColumn: string = undefined,
  ) {}

  public equals(other: Task): boolean {
    // Id is generated by firestore, so it is not compared
    return (
      this.mlModelType === other.mlModelType &&
      this.taskType === other.taskType &&
      this.epochs === other.epochs &&
      this.trainPercentage === other.trainPercentage &&
      this.learningRate === other.learningRate &&
      this.hiddenLayerSizes === other.hiddenLayerSizes &&
      this.seed === other.seed
    );
  }
}
