/* eslint-disable max-len */
import * as functions from "firebase-functions"
// import { DownloadResponse } from "@google-cloud/storage"

/*
 * import fetch from "node-fetch"
 * See: https://stackoverflow.com/a/58734908/11330757
 * Hence using axios instead.
 * Also FormData is now a part of the native Node.js API as of v18 (https://stackoverflow.com/a/73325542/11330757)
 * But Firebase Cloud Function only supports up to v16 -.- 
 */
//const FormData = require("form-data")
import axios from "axios"
import * as admin from "firebase-admin"

admin.initializeApp()

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

/*
function bufferToFile(buffer: Buffer, fileName: string): File {
  return new File([buffer as any], fileName, {
    lastModified: new Date().getTime(),
    type: "text/csv",
  })
}
*/

// Relevant: https://firebase.google.com/docs/storage/extend-with-functions
export async function getNetworksFromStorage(
  userId: string,
  networkId: string
): Promise<Map<string, File>> {
  return new Promise((resolve, reject) => {
    const bucket = admin.storage().bucket()
    const NETWORK_PATH = `Users/${userId}/Networks/${networkId}`
    const networkFiles = new Map<string, File>()
    const NODES_FILE_NAME = `${NETWORK_FILE_TYPE.NODES}.csv`
    const EDGES_FILE_NAME = `${NETWORK_FILE_TYPE.EDGES}.csv`
    console.log(
      `File paths: ${NETWORK_PATH}/${NODES_FILE_NAME}, ${NETWORK_PATH}/${EDGES_FILE_NAME}`
    )
    bucket
      .file(`${NETWORK_PATH}/${NODES_FILE_NAME}`)
      .download()
      .then((nodeFile) => {
        networkFiles.set(
          NETWORK_FILE_TYPE.NODES,
          //bufferToFile(nodeFile[0], NODES_FILE_NAME)
          JSON.parse(JSON.stringify(nodeFile)) // Temporary shitty solution
        )
        console.log(
          `Got ${NODES_FILE_NAME} from storage, size: ${nodeFile.length}`
        )
        bucket
          .file(`${NETWORK_PATH}/${EDGES_FILE_NAME}`)
          .download()
          .then((edgeFile) => {
            networkFiles.set(
              NETWORK_FILE_TYPE.EDGES,
              //bufferToFile(edgeFile[0], EDGES_FILE_NAME)
              JSON.parse(JSON.stringify(edgeFile))
            )
            console.log(
              `Got ${EDGES_FILE_NAME} from storage, size: ${edgeFile.length}`
            )
            resolve(networkFiles)
          })
          .catch((err) => {
            console.log(err)
            reject(err)
          })
      })
      .catch((err) => {
        console.log(err)
        reject(err)
      })
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
      const networkFiles = await getNetworksFromStorage(
        context.params.userId,
        context.params.networkId
      )
      const requestData = {
        nodes: networkFiles.get(NETWORK_FILE_TYPE.NODES),
        edges: networkFiles.get(NETWORK_FILE_TYPE.EDGES),
        task: snap.data(),
      }
      console.log("Request data", requestData)
      /*const f = new FormData()
      f.append(
        NETWORK_FILE_TYPE.NODES,
        networkFiles.get(NETWORK_FILE_TYPE.NODES)!
      )
      f.append(
        NETWORK_FILE_TYPE.EDGES,
        networkFiles.get(NETWORK_FILE_TYPE.EDGES)!
      )
      f.append("task", JSON.stringify(snap.data()))
      console.log("Form data", f)
      */
      // Create an axios get request to the ML service with the task data and content-type as application/json
      const taskResult = await axios.post(ML_SERVICE_URL, requestData, {
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
