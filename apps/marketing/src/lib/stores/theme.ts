import { browser } from '$app/environment'
import { writable } from 'svelte/store'

function createThemeStore() {
    // Get system preference
    const prefersDark = browser && window.matchMedia('(prefers-color-scheme: dark)').matches

    // Use stored preference if exists, otherwise use system preference
    const initialValue = browser
        ? localStorage.theme === 'light'
            ? false
            : localStorage.theme === 'dark'
                ? true
                : prefersDark
        : false

    const { subscribe, set } = writable(initialValue)

    // Set initial class on document
    if (browser) {
        if (initialValue) {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.theme) { // Only update if user hasn't set a preference
                const newValue = e.matches
                document.documentElement.classList.toggle('dark', newValue)
                set(newValue)
            }
        })
    }

    return {
        subscribe,
        toggle: () => {
            if (browser) {
                const isDark = document.documentElement.classList.contains('dark')
                const newValue = !isDark
                localStorage.theme = newValue ? 'dark' : 'light'
                document.documentElement.classList.toggle('dark', newValue)
                set(newValue)
            }
        }
    }
}

export const theme = createThemeStore() 