import { writable, readable } from "svelte/store"
import type { Writable, Readable } from "svelte/store"
import type { Network } from "./definitions/network"
import { MenuItem } from "./definitions/menuItem"
import type { User } from "firebase/auth"
import type { LoginUser } from "./definitions/user"

export const selectedMenuItem: Writable<MenuItem> = writable(MenuItem.HOME)
export const testStoreValue: Writable<string> = writable("test val")
export const netzschleuderNetworkNames: Writable<string[]> = writable([])
export const networksList: Writable<Network[]> = writable([])
export const selectedNetworkIndex: Writable<number> = writable(undefined)

// If there is a network to talk about at all in the list, then
// we can set the selected network index to 0
networksList.subscribe((newNetworksList) => {
  if(newNetworksList.length > 0) {
    selectedNetworkIndex.set(0)
  }
})

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

/*
  userStore holds the current User instance from Firebase Auth.
  It is also used to check if the user is logged in.
  loginUser holds the email and password of the user in localstorage so that the user does not 
  have to login every time. If loginUser is present, the userStore is written accordingly and
  the user is logged in automatically.
*/
export const authUserStore: Writable<User> = writable(undefined)
export const loginUserStore: Writable<LoginUser> = writable(
  localStorage.getItem("loginUser")
    ? JSON.parse(localStorage.getItem("loginUser"))
    : undefined
)
loginUserStore.subscribe((newLoginUser) => {
  if (newLoginUser) {
    localStorage.setItem("loginUser", JSON.stringify(newLoginUser))
  } else {
    localStorage.removeItem("loginUser")
  }
})
