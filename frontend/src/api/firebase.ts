// Import the functions you need from the SDKs you need
import { initializeApp, type FirebaseApp } from "firebase/app"
import {
  collection,
  setDoc,
  addDoc,
  updateDoc,
  deleteDoc,
  getDoc,
  doc,
  query,
  getDocs,
  initializeFirestore,
  DocumentReference,
  onSnapshot,
  Timestamp,
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
  type StorageReference,
} from "firebase/storage"
import firebaseConfig from "../../firebase_config"
import type { LoginUser } from "../definitions/user"
import {
  authUserStore,
  loginUserStore,
  networksList,
  fetchedProfilePicture,
  defaultSeed as defaultSeedStore,
} from "../stores"
import { get } from "svelte/store"
import { Network, Metadata, Node, Link } from "../definitions/network"
import { metadataConverter, tasksConverter } from "./firebase_converters"
import { blobToFile, parseNetwork, removeEmptyFields } from "../util/networkParserUtil"
import type { Task } from "../definitions/task"
import { ExperimentState } from "../definitions/experimentState"

export const app: FirebaseApp = initializeApp(firebaseConfig)
export const db = initializeFirestore(app, {
  experimentalForceLongPolling: true, // this line
})

const enum Database {
  USERS = "Users",
  NETWORKS = "Networks",
  IMAGES = "Images",
  TASKS = "Tasks"
}

export function getCurrentTimestamp(): Timestamp {
  return Timestamp.now()
}

// ---- Authentication ----
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

export async function getDefaultSeed(): Promise<number> {
  return new Promise((resolve, reject) => {
    getDoc(doc(db, Database.USERS, get(authUserStore).uid))
      .then((doc) => {
        if (doc.exists()) {
          resolve(doc.data().defaultSeed)
        } else {
          reject(`No such document for user ${get(authUserStore).uid}!`)
        }
      })
      .catch((error) => reject(error))
  })
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

function getUserPath(): string {
  return `Users/${get(authUserStore).uid}`
}



function getImageStorageRefs(image: string): any {
  const storage = getStorage(app)
  const imagePath = `Users/${get(authUserStore).uid}/Images`
  return {
    imageFileRef: ref(storage, `${imagePath}/${image}.png`),
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
// ---- Authentication ----

export async function UploadProfileImage(imageFile: File): Promise<void> {
  return new Promise((resolve, reject) => {

    const storagePath = getImageStorageRefs('profile')
    uploadBytes(storagePath['imageFileRef'], imageFile)
      .then(() => {
        console.log(`Uploaded image file to firebase`)
        resolve()
      }
      )
      .catch((error) => {
        console.log(`Image upload error: ${error}`)
        reject()
      }
      )
  })
}
// ---- Networks ----
function getNetworkPath(networkId: string): string {
  if (networkId === undefined)
    return `${Database.USERS}/${get(authUserStore).uid}/${Database.NETWORKS}`
  return `${Database.USERS}/${get(authUserStore).uid}/${Database.NETWORKS
    }/${networkId}`
}
function getStorageRefs(
  networkId: string,
  taskId: string | undefined = undefined
): Record<string, StorageReference> {
  /*
  Returns the storage references for the nodes and edges files of a network.
  If taskId is true, the storage references for the task files are returned.
  */
  const storage = getStorage(app)
  const networkPath = getNetworkPath(networkId)
  if (taskId !== undefined) {
    return {
      nodesFileRef: ref(
        storage,
        `${networkPath}/${Database.TASKS}/${taskId}/nodes.csv`
      ),
      edgesFileRef: ref(
        storage,
        `${networkPath}/${Database.TASKS}/${taskId}/edges.csv`
      ),
    }
  }
  return {
    nodesFileRef: ref(storage, `${networkPath}/nodes.csv`),
    edgesFileRef: ref(storage, `${networkPath}/edges.csv`),
  }
}
export async function uploadNetworkToStorage(
  networkMetadata: Metadata = undefined,
  nodesFile: File,
  edgesFile: File,
  taskId: string | undefined = undefined
): Promise<void> {
  return new Promise((resolve, reject) => {
    const storagePaths = getStorageRefs(networkMetadata.id, taskId)
    uploadBytes(storagePaths.nodesFileRef, nodesFile)
      .then(() => {
        console.log(`Uploaded nodes file for network ${networkMetadata.id}`)
        uploadBytes(storagePaths.edgesFileRef, edgesFile)
          .then(() => {
            console.log(`Uploaded edges file for network ${networkMetadata.id}`)
            /*
            If the network is being uploaded for a task, the network metadata
            is not saved to the database, as this is not a network creation task.
            The assumption is that the document for this network under
            Users/{uid}/Networks/{networkId} already exists.
            */
            if (taskId !== undefined) {
              resolve()
            } else {
              saveNetworkDocument(networkMetadata)
                .then(() => {
                  resolve()
                })
                .catch((error) => {
                  reject(error)
                })
            }
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

export async function getProfileImage() {

  const storagePaths = getImageStorageRefs('profile')
  console.log(storagePaths)
  getBlob(storagePaths['imageFileRef']).then((image) => {
    fetchedProfilePicture.set(blobToFile(image, "profileImage.png"))
  })
    .catch((error) => {
      console.log("No file of profilePics")
    }
    )
}

export async function networkExists(networkId: string): Promise<boolean> {
  return new Promise((resolve, reject) => {
    const networkDoc = doc(db, getNetworkPath(networkId))
    getDoc(networkDoc)
      .then((doc) => resolve(doc.exists()))
      .catch((error) => reject(error))
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
            network.nodes = parsedNodes.data
            getBlob(storagePaths.edgesFileRef)
              .then((blob) => {
                parseNetwork(blobToFile(blob, "edges.csv"))
                  .then((parsedEdges) => {
                    network.links = parsedEdges.data
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

function fixNodeFields(data: Node) {
  console.log(data)
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
// ---- Network ----



// ---- Experiments/Tasks ----
export async function setExperimentTask(
  network: Network,
  task: Task
): Promise<string> {
  return new Promise((resolve, reject) => {
    network.nodes = network.nodes.map((node) => { return removeEmptyFields(node) })
    network.links = network.links.map((link) => { return removeEmptyFields(link) })
    let files = network.toFiles()
    addDoc(
      collection(
        db,
        `${getNetworkPath(network.metadata.id)}/${Database.TASKS}`
      ),
      tasksConverter.toFirestore(task)
    )
      .then((taskDoc: DocumentReference) => {
        updateDoc(taskDoc, { id: taskDoc.id }).then(() => {
          console.log(`Added task ${taskDoc.id} to network ${network.metadata.id}`)
          uploadNetworkToStorage(
            network.metadata,
            files.nodes,
            files.links,
            taskDoc.id
          )
            .then(() => {
              updateDefaultSeed(task.seed)
                .then(() => resolve(taskDoc.id))
                .catch((error) => reject(error))
            })
            .catch((error) => reject(error))
        })
          .catch((error) => reject(error))
      }).catch((error) => reject(error))

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

async function updateDefaultSeed(seed: number): Promise<void> {
  return new Promise((resolve, reject) => {
    updateDoc(doc(db, `${Database.USERS}/${get(authUserStore).uid}`), {
      defaultSeed: seed,
    })
      .then(() => {
        defaultSeedStore.set(seed)
        resolve()
      })
      .catch((error) => {
        reject(error)
      })
  })
}

export async function listenForExperimentResult(
  networkId: string,
  taskId: string
): Promise<Task> {
  return new Promise((resolve, reject) => {
    const unsubscribe = onSnapshot(
      doc(db, getNetworkPath(networkId), Database.TASKS, taskId),
      (doc) => {
        // @ts-ignore
        const currentState: ExperimentState = ExperimentState[doc.data().state]
        if (
          [
            ExperimentState.PROGRESS,
            ExperimentState.RESULT,
            ExperimentState.ERROR,
          ].includes(currentState)
        ) {
          if (ExperimentState.PROGRESS === currentState) {
            console.log(`Experiment ${taskId} is in progress. Keep calm and carry on.`)
            return
          } else {
            unsubscribe()
            resolve(tasksConverter.fromFirestore(doc, undefined))
          }
        } else {
          reject(`Invalid experiment state: ${doc.data().state}`)
        }
      }
    )
  })
}
// ---- Experiments/Tasks ----
