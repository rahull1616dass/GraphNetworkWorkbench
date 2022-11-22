import { FileExtension } from "../../../definitions/fileExtension"
import Papa from "papaparse"
import type ParseResult from "papaparse"

export async function parseNetwork(file: File): Promise<ParseResult> {
    let fileExtension: string = file.name.split(".").pop()
    console.log(`File extension: ${fileExtension}`)
    return await new Promise((resolve, reject) => {
        switch (fileExtension) {
            case FileExtension.CSV:
                parseCSV(file)
                    .then((results) => {
                        resolve(results)
                    })
                    .catch((error) => {
                        reject(error)
                    })
                break;

            default:
                break;
        }
    })

}

//Declare an async function that parses a CSV file and returns a promise
async function parseCSV(file: File): Promise<ParseResult> {
    console.log("my name is " + file.name)
    // Parse the CSV file using PapaParse and return a promise
    return await new Promise((resolve, reject) => {
        console.log("my name is in promise" + file.name)
        Papa.parse(file, {
            header: true,
            dynamicTyping: true,
            complete: (results) => {
                // Log the results of PapaParse
                console.log(results)
                resolve(results)
            },
            error: (error) => {
                reject(error)
            }
        })
    })
}

