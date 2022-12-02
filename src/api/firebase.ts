// Import the functions you need from the SDKs you need
import { initializeApp, type FirebaseApp } from "firebase/app"
import { getFirestore, collection, setDoc, doc } from "firebase/firestore"
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithCredential,
  signInWithEmailAndPassword,
} from "firebase/auth"
import firebaseConfig from "../../firebase_config"
import type { User } from "../definitions/user"

export const app: FirebaseApp = initializeApp(firebaseConfig)
export const db = getFirestore(app)

const enum Database {
  USERS = "Users",
}

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
        user.uid = userCredential.user.uid
        setUserDocument(user).then(() => {
          resolve(user)
        })
      })
      .catch((error) => {
        reject(error)
      })
  })
}

export async function loginUser(user: User): Promise<User> {
  return new Promise((resolve, reject) => {
    signInWithEmailAndPassword(getAuth(app), user.email, user.password)
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

async function setUserDocument(user: User): Promise<void> {
  return new Promise((resolve, reject) => {
    setDoc(doc(db, Database.USERS, user.uid), { 
      // Explicitly set the fields rather than using the spread operator
      // to avoid setting the passwords to the document
      email: user.email,
      uid: user.uid
    })
      .then(() => {
        resolve()
      })
      .catch((error) => {
        console.log(`Error setting user.id: ${user.uid} document. ${error}`)
        reject(error)
      })
  })
}
