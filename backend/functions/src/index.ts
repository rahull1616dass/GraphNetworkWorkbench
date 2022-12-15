/* eslint-disable max-len */
import * as functions from "firebase-functions"
import axios from "axios"

/*
 * import fetch from "node-fetch"
 * For some reason, seems fetch does not work for Firebase Cloud Functions.
 * See: https://stackoverflow.com/a/58734908/11330757
 * Hence using axios instead.
 */

const ML_SERVICE_URL = "https://get-prediction-i5wplx5u5a-nw.a.run.app"
const DB = {
  Users: "Users",
  Networks: "Networks",
  Tasks: "Tasks",
}


exports.onTaskCreated = functions.firestore
  .document(
    `${DB.Users}/{userId}/${DB.Networks}/{networkId}/${DB.Tasks}/{taskId}`
  )
  .onCreate(async (snap, context) => {
    console.log("Task created", snap.data())
    console.time("ML Service call")
    try {
      const taskResult = await axios.post(ML_SERVICE_URL, snap.data(), {
        headers: { "Content-Type": "application/json" },
      })
      console.timeEnd("ML Service call")
      console.log("ML Service response", taskResult.data)
    } catch (err) {
      console.log(err)
    }
  })
