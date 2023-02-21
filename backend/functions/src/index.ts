/* eslint-disable max-len */
import * as functions from "firebase-functions"
import { GetSignedUrlResponse, GetSignedUrlConfig } from "@google-cloud/storage"
const cors = require("cors")({ origin: true });

/*
 * import fetch from "node-fetch"
 * See: https://stackoverflow.com/a/58734908/11330757
 * Also request-promise package that the above link recommends is deprecated, lol
 * Hence using axios instead.
 *
 * Also FormData is now a part of the native Node.js API as of v18 (https://stackoverflow.com/a/73325542/11330757)
 * But Firebase Cloud Function only supports up to v16 -.-
 * UPDATE: Using FormData is not necessary anymore, since the ML service can now handle the file URLs directly.
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
    For this to work, the IAM Service Account 2323c   Credentials API needs to be enabled for the project via:
    https://console.cloud.google.com/apis/api/iamcredentials.googleapis.com
    Afterwards, the Service Account Token Creator role needs to be added to the 
    Firebase Admin SDK Service Account.
    */
    const fileReadOptions: GetSignedUrlConfig = {
      version: "v4",
      action: "read",
      expires: Date.now() + (6 * 60 * 60 * 1000), // 6 hours. TODO: In production, set this to a lower time.
      contentType: "text/csv",
    }
    const bucket = admin.storage().bucket()
    const networkFiles = new Map<string, string>()
    const NETWORK_PATH = `Users/${userId}/Networks/${networkId}`
    const NODES_FILE_NAME = `${NETWORK_FILE_TYPE.NODES}.csv`
    const EDGES_FILE_NAME = `${NETWORK_FILE_TYPE.EDGES}.csv`
    console.log(
      `File paths: ${NETWORK_PATH}/${NODES_FILE_NAME}, ${NETWORK_PATH}/${EDGES_FILE_NAME}`
    )
    bucket
      .file(`${NETWORK_PATH}/${NODES_FILE_NAME}`)
      .getSignedUrl(fileReadOptions)
      .then((nodeFileUrl: GetSignedUrlResponse) => {
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
    console.log(
      `Starting task ${context.params.taskId} with task: ${
        snap.data().taskType
      }`
    )
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
      const taskResult = await axios.post(ML_SERVICE_URL, requestData, {
        headers: { "Content-Type": "application/json" },
      })
      console.timeEnd("ML Service call")
      console.log("ML Service response", taskResult.data)
    } catch (err) {
      console.log(err)
    }
  })
  exports.getNetworks = functions.https.onRequest((req, res) => {
    cors(req, res, () => {
      axios
        .get("https://networks.skewed.de/api/nets")
        .then(response => {
          res.send(response.data);
        })
        .catch(error => {
          res.status(500).send(error);
        });
    });
  });

  exports.getNetowrkDescription = functions.https.onRequest((req, res) => {
    cors(req, res, () => {
      const { networkName } = req.query;
      console.log(networkName)
      axios
        .get(`https://networks.skewed.de/api/net/${networkName}`)
        .then(response => {
          res.send(response.data);
        })
        .catch(error => {
          res.status(500).send(error);
        });
    });
  });

  exports.downloadNetworkFile = functions.https.onRequest((req, res) => {
    cors(req, res, () => {
      const { networkName } = req.query;
      const fileUrl = `https://networks.skewed.de/net/${networkName}/files/${networkName}.csv.zip`;
    axios({
      method: "get",
      url: fileUrl,
      responseType: "stream"
    })
      .then(response => {
        res.set("Content-Type", "application/zip");
        res.set(
          "Content-Disposition",
          `attachment; filename=${networkName}.csv.zip`
        );
        response.data.pipe(res);
      })
      .catch(error => {
        console.error(error);
        res.status(500).send(error);
      });
    });
  });