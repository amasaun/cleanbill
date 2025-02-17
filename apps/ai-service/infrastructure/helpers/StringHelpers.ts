export const capitalize = (aString: string): string => {
  const lowered = aString.toLowerCase()
  return `${lowered.charAt(0).toUpperCase()}${lowered.slice(1)}`
}
