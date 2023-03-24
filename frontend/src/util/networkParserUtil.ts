import { FileExtension } from "../definitions/fileExtension"
import Papa from "papaparse"
import type ParseResult from "papaparse"
import { UploadedFileType } from "../definitions/uploadedFileType"
import type JSZip from "jszip"

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
        break

      default:
        break
    }
  })
}

export async function parseReadableStream(
  readableStream: ReadableStream,
  options: any
): Promise<ParseResult> {
  const parseStream = Papa.parse(Papa.NODE_STREAM_INPUT, {})
  readableStream.pipeTo(parseStream)
  let data = []
  parseStream.on("data", (chunk) => {
    data.push(chunk)
  })

  parseStream
    .on("finish", () => {
      console.log(data)
      console.log(data.length)
    })
    .catch((error) => {
      console.log(error)
    })
}


const cleanFieldName = (fieldName: string) => {
  return fieldName.replace(/^[\s#_]+|[\s]+/g, '');
}

async function parseCSV(file: File): Promise<ParseResult> {
  return await new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true,
      transformHeader: (header) => {
        return cleanFieldName(header)
      },
      complete: (results) => {
        if (!results.meta.fields.includes("index")) {
          results.data.forEach((row, index) => {
            row["index"] = index
          })
          results.meta.fields.push("index")
        }
        console.log(results)
        resolve(results)
      },
      error: (error) => {
        reject(error)
      },
    })
  })
}

export function removeEmptyFields(data: any) {
  Object.keys(data).forEach((key) => {
    if (data[key] === null || data[key] === undefined) {
      delete data[key]
    }
  })
  return data
}

export function JSZipObjectToFile(zipObject: JSZip.JSZipObject): Promise<File> {
  return new Promise((resolve, reject) => {
    zipObject.async("blob").then((blob) => {
      resolve(blobToFile(blob, zipObject.name, "text/csv;charset=utf-8;"))
    })
  })
}


export function blobToFile(theBlob: Blob, fileName: string, type: string = undefined): File {
  return new File([theBlob as any], fileName, {
    lastModified: new Date().getTime(),
    type: type === undefined ? theBlob.type: type,
  })
}

export function toCSVFile(
  fileType: UploadedFileType,
  columnNames: string[],
  data: any[]
): File {
  const csv = Papa.unparse({
    fields: columnNames,
    data: data,
  })
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" })
  return new File(
    [blob],
    fileType === UploadedFileType.NODE_FILE ? "nodes.csv" : "edges.csv",
    { type: "text/csv;charset=utf-8;" }
  )
}
