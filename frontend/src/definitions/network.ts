export class Network{
    constructor(
        public metadata: Metadata = new Metadata(),
        public nodes: Node[] = [],
        public links: Link[] = []
    ){}
}


export class Metadata{
    constructor(
        public id: string = undefined,
        public name: string = undefined,
        public description: string = undefined,
        public color: string = undefined
    ){}
}
export class Link{
    constructor(
        readonly source: string = undefined,
        readonly target: string = undefined,
        readonly value: number = undefined
    ){}
}

export class Node{
    constructor(
        public name: string = undefined,
        readonly id: string = undefined,
        readonly group: number = undefined,
        readonly index: number = undefined,
        readonly pos: string[] = undefined
    ){}
}
