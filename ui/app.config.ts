import type { NavItemProps } from "./types/UIProps";

export default defineAppConfig(
    {
        icon: {
            size: '18px', // default <Icon> size applied
            class: 'icon', // default <Icon> class applied
            mode: 'svg', // default <Icon> mode applied
        },
        appName: 'Kontext AI',
        apiBaseUrl: 'http://localhost:8100',
        settingKeys: {
            llmTemperture: 'llm_temperature',
            llmEndpoint: 'llm_endpoint',
            llmApiKey: 'llm_api_key',
            llmDefaultModel: 'llm_default_model',
            username: 'general_username',
        },
        navItems: [
            { id: "home", to: '/', icon: 'material-symbols:home-outline', text: 'Home' },
            {
                id: "tools", icon: 'material-symbols:tools-wrench-outline', text: 'GenAI utils', children: [
                    { id: "newChat", to: '/chat-ollama', icon: 'material-symbols:edit-square-outline', text: 'New chat' },
                    { id: "prompt", to: '/prompt-engineering', icon: 'material-symbols:engineering-outline', text: 'Prompt scratchboard' },
                    { id: "embedding", to: '/embedding-generator', icon: 'material-symbols:question-exchange', text: 'Embedding generator' }
                ]
            },
            // { id: "llmflow", to: '/dashboards', icon: 'material-symbols:linked-services-outline', text: 'Workflows' },
            // { id: "knowledgebase", to: '/dashboards', icon: 'material-symbols:menu-book-outline', text: 'Knowledge base' },
            // { id: "dataSources", to: '/data-sources', icon: 'material-symbols:database-outline', text: 'Data sources' },
            { id: "dataLakes", to: '/data-lakes', icon: 'material-symbols:files-outline', text: 'Datalake' },
            // { id: "databoards", to: '/dashboards', icon: 'material-symbols:dashboard-customize-outline', text: 'Dashboards' },
            { id: "settings", to: '/settings', icon: 'material-symbols:settings-outline', text: 'Settings' },
        ] as NavItemProps[]
    }
)
