import type { Node } from "./network";
export class HoverData{
    constructor(
        readonly node: Node,
        readonly x: number = undefined,
        readonly y: number = undefined,
    ){}
}