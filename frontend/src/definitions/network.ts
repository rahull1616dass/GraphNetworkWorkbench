import { toCSVFile } from "../util/networkParserUtil"
import { UploadedFileType } from "./uploadedFileType"

export class Network{
    constructor(
        public metadata: Metadata = new Metadata(),
        public nodes: object[] = [],
        public links: object[] = []
    ){}

    public toFiles(): Record<string, File> {
        return {
            nodes: toCSVFile(
                UploadedFileType.NODE_FILE,
                Object.keys(this.nodes[0]),
                this.nodes
              ),
            links: toCSVFile(
                UploadedFileType.EDGE_FILE,
                Object.keys(this.links[0]),
                this.links
              )
        }
    }
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
        //readonly value: (string|number)[] = undefined,
        //readonly __parsed_extra: object = undefined,
    ){}

    public equals(other: Link): boolean{
        // Cruically, the value need not be equal for the links to be equal
        return this.source === other.source &&
            this.target === other.target
    }
}

export class Node{
    constructor(
        public name: string = undefined,
        //readonly id: string = undefined,
        readonly group: number = undefined,
        readonly index: number = undefined,
        //readonly pos: string[] = undefined,
        public is_train: number = undefined,
        //readonly __parsed_extra: object = undefined,
    ){}
}
