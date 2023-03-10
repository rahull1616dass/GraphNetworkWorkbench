/*
Defines the FetchableNetwork class, which is used to fetch network descriptions
and to generate their download URLs.
For now, only netzschleuder networks are supported.
*/
export class FetchableNetwork {
    constructor(
        public networkName: string = undefined,
        public subNetworkName: string = undefined,
        public content: string = undefined,
    ) { }

    public getNetworkContentEndpoint() {
        return `https://us-central1-graphlearningworkbench.cloudfunctions.net/getNetworkDescription?networkName=${this.networkName}`
    }

    public getDownloadEndpoint() {
        if (this.subNetworkName === undefined) this.subNetworkName = this.networkName
        return `https://us-central1-graphlearningworkbench.cloudfunctions.net/downloadNetworkFile?networkName=${this.networkName}&netName=${this.subNetworkName}`
    }

    public getNetworkName() {
        return this.subNetworkName === undefined ? `${this.networkName}_${this.networkName}` :
            `${this.networkName}_${this.subNetworkName}`
    }
}