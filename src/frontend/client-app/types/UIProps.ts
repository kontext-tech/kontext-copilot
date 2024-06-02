export interface NavItemProps {
    id: string
    to?: string
    icon: string
    text: string
    children?: NavItemProps[]
}
