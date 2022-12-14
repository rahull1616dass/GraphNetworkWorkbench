/* eslint-disable max-len */
import * as functions from "firebase-functions"

// Create a const typescript object to store the collection names

const DB = {
  Users: "Users",
  Networks: "Networks",
  Tasks: "Tasks",
}

exports.onTaskCreated = functions.firestore
    .document(`${DB.Users}/{userId}/${DB.Networks}/{networkId}/${DB.Tasks}/{taskId}`)
    .onCreate((snap, context) => {
      console.log("Task created", snap.data())
    })
