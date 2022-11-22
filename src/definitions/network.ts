export class Network{
    constructor(
        public metadata: Metadata = new Metadata(),
        public nodes: Node[] = [],
        public links: Link[] = []
    ){}
}


export class Metadata{
    constructor(
        public name: string,
        public description: string
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
        readonly name: string,
        readonly id: string,
        readonly group: number,
        readonly index: number,
        readonly pos: Array<string>
    ){}
}
