export default async function request(
  url: string,
  options: RequestInit = {},
  should_return_json = true
): Promise<any> {
  return await new Promise((resolve, reject) => {
    fetch(url, options)
      .then((response) => {
        if (response.ok) {
          if (should_return_json) {
            return response.json()
          } else {
            return response
          }
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
