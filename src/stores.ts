import {  writable } from "svelte/store"
import type { Writable } from "svelte/store"

export const test_store_value: Writable<string> = writable("test val")