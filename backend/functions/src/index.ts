/* eslint-disable max-len */
import * as functions from "firebase-functions"
import { GetSignedUrlResponse, GetSignedUrlConfig } from "@google-cloud/storage"

/*
 * import fetch from "node-fetch"
 * See: https://stackoverflow.com/a/58734908/11330757
 * Hence using axios instead.
 * Also FormData is now a part of the native Node.js API as of v18 (https://stackoverflow.com/a/73325542/11330757)
 * But Firebase Cloud Function only supports up to v16 -.-
 */

import axios from "axios"
import * as admin from "firebase-admin"

admin.initializeApp()

const NETWORK_FILE_TYPE = {
  NODES: "nodes",
  EDGES: "edges",
}
const ML_SERVICE_URL = "https://get-prediction-i5wplx5u5a-oa.a.run.app"
const DB = {
  Users: "Users",
  Networks: "Networks",
  Tasks: "Tasks",
}

// Relevant: https://firebase.google.com/docs/storage/extend-with-functions
export async function getNetworksFromStorage(
  userId: string,
  networkId: string
): Promise<Map<string, string>> {
  return new Promise((resolve, reject) => {
    /*
    Why go into the trouble of getting the file URLs here, rather than having them saved
    in the document anyway, when the file is being uploaded in the front-end?
    For security reasons. This way, the file URLs are temporary, and will expire after a certain time.
    For this to work, the IAM Service Account Credentials API needs to be enabled for the project via:
    https://console.cloud.google.com/apis/api/iamcredentials.googleapis.com
    Afterwards, the Service Account Token Creator role needs to be added to the 
    Firebase Admin SDK Service Account.
    */
    const fileReadOptions: GetSignedUrlConfig = {
      version: "v4",
      action: "read",
      expires: Date.now() + 15 * 60 * 1000, // 15 minutes
      contentType: "text/csv",
    }
    const bucket = admin.storage().bucket()
    const NETWORK_PATH = `Users/${userId}/Networks/${networkId}`
    const networkFiles = new Map<string, string>()
    const NODES_FILE_NAME = `${NETWORK_FILE_TYPE.NODES}.csv`
    const EDGES_FILE_NAME = `${NETWORK_FILE_TYPE.EDGES}.csv`
    console.log(
      `File paths: ${NETWORK_PATH}/${NODES_FILE_NAME}, ${NETWORK_PATH}/${EDGES_FILE_NAME}`
    )
    bucket
      .file(`${NETWORK_PATH}/${NODES_FILE_NAME}`)
      .getSignedUrl(fileReadOptions)
      .then((nodeFileUrl: GetSignedUrlResponse) => {
        console.log(`file: ${nodeFileUrl}`)
        console.log(`file[0]: ${nodeFileUrl[0]}`)
        networkFiles.set(NETWORK_FILE_TYPE.NODES, nodeFileUrl[0])
        bucket
          .file(`${NETWORK_PATH}/${EDGES_FILE_NAME}`)
          .getSignedUrl(fileReadOptions)
          .then((edgeFileUrl: GetSignedUrlResponse) => {
            networkFiles.set(NETWORK_FILE_TYPE.EDGES, edgeFileUrl[0])
            resolve(networkFiles)
          })
          .catch((err) => reject(err))
      })
      .catch((err) => reject(err))
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
        nodesFileUrl: networkFiles.get(NETWORK_FILE_TYPE.NODES),
        edgesFileUrl: networkFiles.get(NETWORK_FILE_TYPE.EDGES),
        task: snap.data(),
      }
      console.log("Request data", requestData)
      // Create an axios get request to the ML service with the task data and content-type as application/json
      const taskResult = await axios.post(ML_SERVICE_URL, requestData, {
        headers: { "Content-Type": "application/json" },
      })

      console.timeEnd("ML Service call")
      console.log("ML Service response", taskResult.data)
    } catch (err) {
      console.log(err)
    }
  })
