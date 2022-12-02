// Import the functions you need from the SDKs you need
import { initializeApp, type FirebaseApp } from "firebase/app"
import { getFirestore, collection, addDoc } from "firebase/firestore"
import firebaseConfig from "../../firebase_config"

export const app: FirebaseApp = initializeApp(firebaseConfig)
export const db = getFirestore(app)

export async function addDocument(){
    try {
        const docRef = await addDoc(collection(db, "users"), {
          first: "Ada",
          last: "Lovelace",
          born: 1815
        });
        console.log("Document written with ID: ", docRef.id);
      } catch (e) {
        console.error("Error adding document: ", e);
      }
}
