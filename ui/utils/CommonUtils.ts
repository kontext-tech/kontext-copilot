export const isEmptyOrNull = (str: string | null): boolean => {
    return str === null || str.trim() === ''
}
