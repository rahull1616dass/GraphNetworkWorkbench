/* eslint-disable max-len */
import * as functions from "firebase-functions"
/*
 * import fetch from "node-fetch"
 * For some reason, seems fetch does not work for Firebase Cloud Functions.
 * See: https://stackoverflow.com/a/58734908/11330757
 * Hence using axios instead.
 */
import axios from "axios"
import * as admin from "firebase-admin"
import { initializeApp } from "firebase-admin/app"

class NetworkFile {
  constructor(public storageRef: string, public file: File | null) {}
}

const NETWORK_FILE_TYPE = {
  NODES: "nodes",
  EDGES: "edges",
}
const ML_SERVICE_URL = "https://get-prediction-i5wplx5u5a-nw.a.run.app"
const DB = {
  Users: "Users",
  Networks: "Networks",
  Tasks: "Tasks",
}
const app = initializeApp()

function blobToFile(theBlob: Blob, fileName: string): File {
  return new File([theBlob as any], fileName, {
    lastModified: new Date().getTime(),
    type: theBlob.type,
  })
}

// Relevant: https://firebase.google.com/docs/storage/extend-with-functions
export async function getNetworkFromStorage(
  userId: string,
  networkId: string
): Promise<Map<string, File>> {
  return new Promise((resolve, reject) => {
    const bucket = admin.storage().bucket()
    const networkPath = `Users/${userId}/Networks/${networkId}`
    const networkFiles = new Map<string, File>()
    const nodesFileName = `${NETWORK_FILE_TYPE.NODES}.csv`
    const edgesFileName = `${NETWORK_FILE_TYPE.EDGES}.csv`
    getBlob(ref(getStorage(), `${networkPath}/${nodesFileName}`))
      .then((blob: Blob) => {
        console.log(`Got blob for ${nodesFileName}, ${blob.size} bytes`)
        networkFiles.set(
          NETWORK_FILE_TYPE.NODES,
          blobToFile(blob, nodesFileName)
        )

        getBlob(ref(getStorage(), `${networkPath}/${edgesFileName}`))
          .then((blob: Blob) => {
            console.log(`Got blob for ${edgesFileName}, ${blob.size} bytes`)
            networkFiles.set(
              NETWORK_FILE_TYPE.EDGES,
              blobToFile(blob, edgesFileName)
            )
            resolve(networkFiles)
          })
          .catch((error: any) => {
            reject(error)
          })
      })
      .catch((error: any) => reject(error))
  })
}

exports.onTaskCreated = functions.firestore
  .document(
    `${DB.Users}/{userId}/${DB.Networks}/{networkId}/${DB.Tasks}/{taskId}`
  )
  .onCreate(async (snap, context) => {
    console.log("Task created", snap.data())
    console.time("ML Service call")
    try {
      const networkFiles = await getNetworkFromStorage(
        context.params.userId,
        context.params.networkId
      )
      const formData = new FormData()
      formData.append(
        NETWORK_FILE_TYPE.NODES,
        networkFiles.get(NETWORK_FILE_TYPE.NODES)!
      )
      formData.append(
        NETWORK_FILE_TYPE.EDGES,
        networkFiles.get(NETWORK_FILE_TYPE.EDGES)!
      )
      formData.append("task", JSON.stringify(snap.data()))

      // Create an axios get request to the ML service with the task data and content-type as application/json
      const taskResult = await axios.post(ML_SERVICE_URL, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })

      console.timeEnd("ML Service call")
      console.log("ML Service response", taskResult.data)
      console.timeEnd("ML Service call")
      console.log("ML Service response", taskResult.data)
    } catch (err) {
      console.log(err)
    }
  })
