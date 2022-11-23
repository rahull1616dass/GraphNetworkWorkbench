export class Network{
    constructor(
        public metadata: Metadata = new Metadata(),
        public nodes: Node[] = [],
        public links: Link[] = []
    ){}
}


export class Metadata{
    constructor(
        public name: string = undefined,
        public description: string = undefined
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
        readonly name: string = undefined,
        readonly id: string = undefined,
        readonly group: number = undefined,
        readonly index: number = undefined,
        readonly pos: string[] = undefined
    ){}
}
