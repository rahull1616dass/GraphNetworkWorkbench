import {  writable } from "svelte/store"
import type { Writable } from "svelte/store"

export const testStoreValue: Writable<string> = writable("test val")

export const netzschleuderNetworkNames: Writable<Array<string>> = writable(new Array())