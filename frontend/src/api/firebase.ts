// Import the functions you need from the SDKs you need
import { initializeApp, type FirebaseApp } from "firebase/app"
import {
  getFirestore,
  collection,
  setDoc,
  doc,
  query,
  getDocs,
  initializeFirestore,
} from "firebase/firestore"
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
  getBlob,
} from "firebase/storage"
import firebaseConfig from "../../firebase_config"
import type { LoginUser } from "../definitions/user"
import { authUserStore, loginUserStore, networksList, fetchedProfilePicture } from "../stores"
import { get } from "svelte/store"
import { Network, type Metadata, Node, Link } from "../definitions/network"
import { metadataConverter } from "./firebase_converters"
import {
  blobToFile,
  parseNetwork,
} from "../components/pages/AddNetwork/UploadNetwork/networkParser"
export const app: FirebaseApp = initializeApp(firebaseConfig)
export const db = initializeFirestore(app, {
  experimentalForceLongPolling: true, // this line
})

const enum Database {
  USERS = "Users",
  NETWORKS = "Networks",
  IMAGES = "Images"
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

function getStorageRefs(networkId: string): any {
  const storage = getStorage(app)
  const networkPath = `Users/${get(authUserStore).uid}/Networks/${networkId}`
  return {
    nodeFileRef: ref(storage, `${networkPath}/nodes.csv`),
    edgesFileRef: ref(storage, `${networkPath}/edges.csv`),
  }
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
    signInWithEmailAndPassword(getAuth(app), loginUser.email, loginUser.password)
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

export async function UploadProfileImage(imageFile: File):Promise<void>
{
  return new Promise((resolve, reject)=> {

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

export async function uploadNetworkToStorage(
  networkMetadata: Metadata,
  nodesFile: File,
  edgesFile: File
): Promise<void> {
  return new Promise((resolve, reject) => {
    const storagePaths = getStorageRefs(networkMetadata.id)
    uploadBytes(storagePaths['nodeFileRef'], nodesFile)
      .then((nodesFileSnapshot) => {
        console.log(`Uploaded nodes file for network ${networkMetadata.id}`)
        uploadBytes(storagePaths['edgesFileRef'], edgesFile)
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
    const docPath = `${Database.USERS}/${get(authUserStore).uid}/${
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

export async function getProfileImage() {
  
  const storagePaths = getImageStorageRefs('profile')
  console.log(storagePaths)
  getBlob(storagePaths['imageFileRef']).then((image) => {
    fetchedProfilePicture.set(blobToFile(image, "profileImage.png"))
  })
  .catch((error) => 
  {
    console.log("No file of profilePics")
  }
  )
}

export async function getNetworks() {
  const networksQuery = query(
    collection(
      db,
      `${Database.USERS}/${get(authUserStore).uid}/${Database.NETWORKS}`
    )
  )
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
    getBlob(storagePaths['nodeFileRef'])
      .then((blob) => {
        console.log(blob)
        parseNetwork(blobToFile(blob, "nodes.csv"))
          .then((parsedNodes) => {
            network.nodes = <Node[]>(
              JSON.parse(JSON.stringify(parsedNodes.data))
            )
            getBlob(storagePaths['edgesFileRef'])
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
