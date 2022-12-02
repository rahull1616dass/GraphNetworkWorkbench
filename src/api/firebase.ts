// Import the functions you need from the SDKs you need
import { initializeApp, type FirebaseApp } from "firebase/app"
import { getFirestore, collection, addDoc } from "firebase/firestore"
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth"
import firebaseConfig from "../../firebase_config"
import type { User } from "../definitions/user"

export const app: FirebaseApp = initializeApp(firebaseConfig)
export const db = getFirestore(app)

export async function addDocument() {
  try {
    const docRef = await addDoc(collection(db, "users"), {
      first: "Ada",
      last: "Lovelace",
      born: 1815,
    })
    console.log("Document written with ID: ", docRef.id)
  } catch (e) {
    console.error("Error adding document: ", e)
  }
}

export async function registerUser(user: User): Promise<User> {
   return new Promise((resolve, reject) => {
      createUserWithEmailAndPassword(getAuth(app), user.email, user.password)
          .then((userCredential) => {
              // Signed in
              const signedInUser = userCredential.user  
              resolve(user)
          })
          .catch((error) => {
              reject(error)
          })
    })
}

