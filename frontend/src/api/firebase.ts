// Import the functions you need from the SDKs you need
import { initializeApp, type FirebaseApp } from "firebase/app"
import {
  collection,
  setDoc,
  addDoc,
  deleteDoc,
  doc,
  query,
  getDocs,
  initializeFirestore,
} from "firebase/firestore"
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "firebase/auth"
import {
  getStorage,
  ref,
  uploadBytes,
  getBlob,
  deleteObject,
} from "firebase/storage"
import firebaseConfig from "../../firebase_config"
import type { LoginUser } from "../definitions/user"
import { authUserStore, loginUserStore, networksList } from "../stores"
import { get } from "svelte/store"
import { Network, type Metadata, Node, Link } from "../definitions/network"
import { metadataConverter, tasksConverter } from "./firebase_converters"
import {
  blobToFile,
  parseNetwork,
} from "../helper/networkParser"
import type { Task } from "../definitions/task"

export const app: FirebaseApp = initializeApp(firebaseConfig)
export const db = initializeFirestore(app, {
  experimentalForceLongPolling: true, // this line
})

const enum Database {
  USERS = "Users",
  NETWORKS = "Networks",
  TASKS = "Tasks",
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
          authUserStore.set(userCredential.user)
          loginUserStore.set(loginUser)
          resolve()
        })
      })
      .catch((error) => {
        reject(error)
      })
  })
}

function getNetworkPath(networkId: string): string {
  if (networkId === undefined) return `Users/${get(authUserStore).uid}/Networks`
  return `Users/${get(authUserStore).uid}/Networks/${networkId}`
}

function getStorageRefs(networkId: string): any {
  const storage = getStorage(app)
  const networkPath = getNetworkPath(networkId)
  return {
    nodesFileRef: ref(storage, `${networkPath}/nodes.csv`),
    edgesFileRef: ref(storage, `${networkPath}/edges.csv`),
  }
}

export async function loginUser(loginUser: LoginUser): Promise<LoginUser> {
  return new Promise((resolve, reject) => {
    signInWithEmailAndPassword(
      getAuth(app),
      loginUser.email,
      loginUser.password
    )
      .then((userCredential) => {
        // Signed in
        authUserStore.set(userCredential.user)
        loginUserStore.set(loginUser)
        resolve(loginUser)
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
  return new Promise((resolve, reject) => {
    const storagePaths = getStorageRefs(networkMetadata.id)
    uploadBytes(storagePaths.nodesFileRef, nodesFile)
      .then((nodesFileSnapshot) => {
        console.log(`Uploaded nodes file for network ${networkMetadata.id}`)
        uploadBytes(storagePaths.edgesFileRef, edgesFile)
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
    setDoc(
      doc(db, getNetworkPath(networkMetadata.id)),
      metadataConverter.toFirestore(networkMetadata)
    )
      .then(() => {
        resolve()
      })
      .catch((error) => {
        reject(error)
      })
  })
}

export async function getNetworks() {
  const networksQuery = query(collection(db, getNetworkPath(undefined)))
  await getDocs(networksQuery).then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
      const metadata = metadataConverter.fromFirestore(doc, undefined)
      getNetworkFromStorage(metadata).then((network) => {
        networksList.set([...get(networksList), network])
        console.log(metadata)
      })
    })
  })
}

export async function getNetworkFromStorage(
  metadata: Metadata
): Promise<Network> {
  return new Promise((resolve, reject) => {
    let network: Network = new Network(metadata)
    const storagePaths = getStorageRefs(metadata.id)
    getBlob(storagePaths.nodesFileRef)
      .then((blob) => {
        console.log(blob)
        parseNetwork(blobToFile(blob, "nodes.csv"))
          .then((parsedNodes) => {
            network.nodes = <Node[]>JSON.parse(JSON.stringify(parsedNodes.data))
            getBlob(storagePaths.edgesFileRef)
              .then((blob) => {
                parseNetwork(blobToFile(blob, "edges.csv"))
                  .then((parsedEdges) => {
                    network.links = <Link[]>(
                      JSON.parse(JSON.stringify(parsedEdges.data))
                    )
                    resolve(network)
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
      .catch((error) => {
        reject(error)
      })
  })
}

export async function setExperimentTask(
  networkId: string,
  task: Task
): Promise<void> {
  return new Promise((resolve, reject) => {
    addDoc(
      collection(db, `${getNetworkPath(networkId)}/${Database.TASKS}`),
      tasksConverter.toFirestore(task)
    )
      .then(() => {
        resolve()
      })
      .catch((error) => {
        console.log(
          `Error setting experiment task for network ${networkId}. ${error}`
        )
        reject(error)
      })
  })
}

export async function getExperimentTasks(networkId: string): Promise<Task[]> {
  return new Promise((resolve, reject) => {
    const tasksQuery = query(
      collection(db, getNetworkPath(networkId), Database.TASKS)
    )
    getDocs(tasksQuery)
      .then((querySnapshot) => {
        let tasks: Task[] = []
        querySnapshot.forEach((doc) => {
          tasks.push(tasksConverter.fromFirestore(doc, undefined))
        })
        resolve(tasks)
      })
      .catch((error) => {
        console.log(
          `Error getting experiment tasks for network ${networkId}. ${error}`
        )
        reject(error)
      })
  })
}

export async function deleteNetwork(networkId: string): Promise<void> {
  return new Promise((resolve, reject) => {
    deleteDoc(doc(db, getNetworkPath(networkId))).then(() => {
      console.log(`Deleted network document ${networkId}`)
      const storageRefs = getStorageRefs(networkId)
      deleteObject(storageRefs.nodesFileRef)
        .then(() => {
          console.log(`Deleted network nodes file ${networkId}`)
          deleteObject(storageRefs.edgesFileRef)
            .then(() => {
              console.log(`Deleted network edges file ${networkId}`)
              resolve()
            })
            .catch((error) => {
              console.log(
                `Error deleting network edges file ${networkId}. ${error}`
              )
              reject(error)
            })
        })
        .catch((error) => {
          console.log(
            `Error deleting network nodes file ${networkId}. ${error}`
          )
          reject(error)
        })
        .catch((error) => {
          console.log(`Error deleting network document ${networkId}. ${error}`)
          reject(error)
        })
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
