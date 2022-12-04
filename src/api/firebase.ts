// Import the functions you need from the SDKs you need
import { initializeApp, type FirebaseApp } from "firebase/app"
import { getFirestore, collection, setDoc, doc } from "firebase/firestore"
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithCredential,
  signInWithEmailAndPassword,
} from "firebase/auth"
import {
  getStorage,
  ref,
  uploadBytes,
  type StorageReference,
} from "firebase/storage"
import firebaseConfig from "../../firebase_config"
import type { LoginUser } from "../definitions/user"
import { userStore } from "../stores"
import { get } from "svelte/store"
import type { Metadata } from "../definitions/network"
import { metadataConverter } from "./firebase_converters"

export const app: FirebaseApp = initializeApp(firebaseConfig)
export const db = getFirestore(app)

const enum Database {
  USERS = "Users",
  NETWORKS = "Networks",
}

export async function registerUser(loginUser: LoginUser): Promise<void> {
  return new Promise((resolve, reject) => {
    createUserWithEmailAndPassword(
      getAuth(app),
      loginUser.email,
      loginUser.password
    )
      .then((userCredential) => {
        // Signed in
        loginUser.uid = userCredential.user.uid
        setUserDocument(loginUser).then(() => {
          userStore.set(userCredential.user)
          resolve()
        })
      })
      .catch((error) => {
        reject(error)
      })
  })
}

export async function loginUser(user: LoginUser): Promise<LoginUser> {
  return new Promise((resolve, reject) => {
    signInWithEmailAndPassword(getAuth(app), user.email, user.password)
      .then((userCredential) => {
        // Signed in
        const signedInUser = userCredential.user
        userStore.set(userCredential.user)
        resolve(user)
      })
      .catch((error) => {
        reject(error)
      })
  })
}

export async function uploadNetworkToStorage(
  networkMetadata: Metadata,
  nodesFile: File,
  edgesFile: File
): Promise<void> {
  const storage = getStorage(app)
  return new Promise((resolve, reject) => {
    const networkPath: string = `Users/${get(userStore).uid}/Networks/${
      networkMetadata.id
    }`
    const nodesFileRef: StorageReference = ref(
      storage,
      `${networkPath}/nodes.csv`
    )
    const edgesFileRef: StorageReference = ref(
      storage,
      `${networkPath}/edges.csv`
    )
    uploadBytes(nodesFileRef, nodesFile)
      .then((nodesFileSnapshot) => {
        console.log(`Uploaded nodes file for network ${networkMetadata.id}`)
        uploadBytes(edgesFileRef, edgesFile)
          .then((edgesFileSnapshot) => {
            console.log(`Uploaded edges file for network ${networkMetadata.id}`)
            saveNetworkDocument(networkMetadata)
              .then(() => {
                resolve()
              })
              .catch((error) => {
                reject(error)
              })
          })
          .catch((error) => {
            reject(error)
          })
      })
      .catch((error) => {
        reject(error)
      })
  })
}

async function saveNetworkDocument(networkMetadata: Metadata): Promise<void> {
  return new Promise((resolve, reject) => {
    const docPath = `${Database.USERS}/${get(userStore).uid}/${
      Database.NETWORKS
    }/${networkMetadata.id}`
    setDoc(doc(db, docPath), metadataConverter.toFirestore(networkMetadata))
      .then(() => {
        resolve()
      })
      .catch((error) => {
        reject(error)
      })
  })
}

async function setUserDocument(user: LoginUser): Promise<void> {
  return new Promise((resolve, reject) => {
    setDoc(doc(db, Database.USERS, user.uid), {
      // Explicitly set the fields rather than using the spread operator
      // to avoid setting the passwords to the document
      email: user.email,
      uid: user.uid,
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
