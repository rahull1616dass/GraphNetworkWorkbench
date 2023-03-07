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

export function removeCSVColumns(csvData, columnsToRemove) {
  const rows = csvData.split("\n").map(row => {
    const cells = [];
    let cell = "";
    let insideQuote = false;
    for (let char of row) {
      if (char === '"') {
        insideQuote = !insideQuote;
      } else if (char === "," && !insideQuote) {
        cells.push(cell);
        cell = "";
      }
      else if(char ===","&&insideQuote)
      {
        cell+='_'
      }
      else {
        cell += char;
      }
    }
    cells.push(cell);
    return cells;
  });
  const header = rows[0];
  let indicesToRemove = [];
  if (Array.isArray(columnsToRemove)) {
    for (const col of columnsToRemove) {
      const index = header.indexOf(col);
      if (index !== -1) {
        indicesToRemove.push(index);
      }
    }
  }
  return rows.map(row => {
    return row.filter((_, i) => !indicesToRemove.includes(i));
  }).map(row => row.join(",")).join("\n");
}

//Declare an async function that parses a CSV file and returns a promise
async function parseCSV(file: File): Promise<ParseResult> {
  console.log("my name is " + file.name)
  // Parse the CSV file using PapaParse and return a promise
  return await new Promise((resolve, reject) => {
    console.log("my name is in promise" + file.name)
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true,
      complete: (results) => {
        // Log the results of PapaParse
        console.log(results)
        resolve(results)
      },
      error: (error) => {
        reject(error)
      },
    })
  })
}


export function parseNetzschleuderFile(blob: Blob, uploadedFileType: UploadedFileType): Promise<File> {
  return new Promise((resolve, reject) => {
    Papa.parse(blob, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true,
      complete: (results) => {
        // Log the results of PapaParse
        console.log(results)
        resolve(results)
      },
      error: (error) => {
        reject(error)
      },
    })
  })
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
