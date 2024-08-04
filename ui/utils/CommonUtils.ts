export const isEmptyOrNull = (str: string | null): boolean => {
   return str === null || str.trim() === ""
}

export const getBaseUrl = (apiBaseUrl: string) => {
   return `${apiBaseUrl}/api`
}
