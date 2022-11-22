export class ErrorData{
    constructor(
        public messageHeader: string = "Error",
        public messageBody: string = "I'm a very generic error message. Please fill me with a more specific error message.",
        public isOpen: boolean = false 
    ){}
}