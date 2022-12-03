import { writable, readable } from "svelte/store"
import type { Writable, Readable } from "svelte/store"
import type { Network } from "./definitions/network"
import { MenuItem } from "./definitions/menuItem"
import type { User } from "firebase/auth"

export const selectedMenuItem: Writable<MenuItem> = writable(MenuItem.HOME)
export const testStoreValue: Writable<string> = writable("test val")
export const netzschleuderNetworkNames: Writable<string[]> = writable([])
export const networksList: Writable<Network[]> = writable([])
export const paletteColors: Readable<string[]> = readable([
  "#1f77b4",
  "#ff7f0e",
  "#2ca02c",
  "#d62728",
  "#9467bd",
  "#8c564b",
  "#e377c2",
  "#7f7f7f",
  "#bcbd22",
  "#17becf",
])
export const userStore: Writable<User> = writable(undefined)
