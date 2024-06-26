import { useStorage } from '@vueuse/core'

export default function useUsername() {
    const config = useAppConfig()
    const username = useStorage(config.settingKeys.username, 'Kontext User')

    return username
}