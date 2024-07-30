import type { NavItemProps } from "~/types/UIProps"

export default function usePageTitle() {
    const config = useAppConfig()
    const route = useRoute()
    const pageTitle = ref(config.appName)

    // Function to flatten the navItems array
    function flattenNavItems(items: NavItemProps[]): NavItemProps[] {
        return items.reduce<NavItemProps[]>((acc, item) => {
            const { children, ...rest } = item
            acc.push(rest) // Add the current item without children to the accumulator
            if (children && children.length) {
                acc.push(...flattenNavItems(children)) // Recursively flatten and add children
            }
            return acc
        }, [])
    }

    // Flattened navItems array
    const flatNavItems = flattenNavItems(config.navItems)

    watchEffect(() => {
        const nav = flatNavItems.find(r => r.to === route.path)
        pageTitle.value = nav ? nav.text : config.appName
        route.meta['title'] = pageTitle.value
    })

    return pageTitle
}
