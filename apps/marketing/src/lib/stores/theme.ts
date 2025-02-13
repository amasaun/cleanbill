import { browser } from '$app/environment'
import { writable } from 'svelte/store'

function createThemeStore() {
    const { subscribe, set } = writable(false)

    if (browser) {
        // Initial setup
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)')

        const setTheme = (dark: boolean) => {
            document.documentElement.classList.toggle('dark', dark)
            set(dark)
        }

        // Set initial theme
        if (localStorage.theme === 'dark') {
            setTheme(true)
        } else if (localStorage.theme === 'light') {
            setTheme(false)
        } else {
            setTheme(systemDark.matches)
        }

        // Listen for system theme changes
        systemDark.addEventListener('change', (e) => {
            if (!localStorage.theme) {
                setTheme(e.matches)
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