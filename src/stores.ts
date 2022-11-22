import {  writable } from "svelte/store"
import type { Writable } from "svelte/store"
import type { Network } from "./definitions/network"
import { MenuItem } from "./definitions/menuItem"

export const selectedMenuItem: Writable<MenuItem> = writable(MenuItem.HOME)
export const testStoreValue: Writable<string> = writable("test val")
export const netzschleuderNetworkNames: Writable<string[]> = writable([])
export const networksList: Writable<Network[]> = writable([])