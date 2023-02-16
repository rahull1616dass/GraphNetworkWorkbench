// Various util functions that can be used throughout the app, without necessarily
// being part of any component/object.
export async function delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
}