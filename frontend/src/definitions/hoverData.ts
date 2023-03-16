import type { Node, Link } from "./network"
import type { HoverType } from "./hoverType"
export class HoverData{
    constructor(
        readonly type: HoverType,
        readonly link: Link,
        readonly node: Node,
        readonly x: number = undefined,
        readonly y: number = undefined,
        readonly is_train: boolean = undefined,
    ){}
}