export class Network{
    constructor(
        readonly nodes: Node[],
        readonly links: Link[]
    ){}
}

export class Link{
    constructor(
        readonly source: string,
        readonly target: string,
        readonly value: number
    ){}
}

export class Node{
    constructor(
        readonly id: string,
        readonly group: number
    ){}
}
