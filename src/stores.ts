import {  writable } from "svelte/store"
import type { Writable } from "svelte/store"
import type { Network } from "./definitions/network"
export const testStoreValue: Writable<string> = writable("test val")
export const networksList: Writable<Network[]> = writable(new Array())
export const netzschleuderNetworkNames: Writable<string[]> = writable(new Array())