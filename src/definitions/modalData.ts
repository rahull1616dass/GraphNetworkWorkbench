export class ModalData{
    constructor(
        public object: any = null,
        public messageHeader: string = "Error",
        public messageBody: string = "I'm a very generic message. Please fill me with a more specific error message.",
        public isOpen: boolean = false 
    ){}
}