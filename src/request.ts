export default async function request(
  url: string,
  options: RequestInit = {}
): Promise<any> {
  return await new Promise((resolve, reject) => {
    fetch(url, options)
      .then((response) => {
        if (response.ok) {
          return response.json()
        } else {
          throw `Server error: [${response.status}] [${response.statusText}] [${response.url}]`
        }
      })
      .then((json) => {
        console.log("Result: ", json)
        resolve(json)
      })
      .catch((error) => {
        reject(error)
      })
  })
}
