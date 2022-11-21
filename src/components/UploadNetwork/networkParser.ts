import { FileExtension } from "./fileExtension"
import Papa from "papaparse"


export default function parseNetwork(file: File) {
    let fileExtension: string = file.name.split(".").pop()
    console.log(`File extension: ${file}`)
    switch (fileExtension) {
        case FileExtension.CSV:
            parseCSV(file)
            break;

        default:
            break;
    }
}

function parseCSV(file: File) {
    Papa.parse(file, {
        complete: function (results) {
            console.log("Finished:", results.data);
        }
    })
}