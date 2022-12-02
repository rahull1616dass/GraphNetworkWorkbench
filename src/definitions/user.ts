export class User {
    constructor(
        public uid: string = "",
        public email: string = "",
        public password: string = "",
        public passwordConfirm: string = "",
    ) { }
}

export interface UserLogin {
    email: string
    password: string
    passwordConfirm: string
}