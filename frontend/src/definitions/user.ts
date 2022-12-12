export class LoginUser {
    constructor(
        public uid: string = "",
        public email: string = "",
        public password: string = "",
        public passwordConfirm: string = "",
    ) { }
}