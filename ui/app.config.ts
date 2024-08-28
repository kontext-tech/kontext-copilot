import type { NavItemProps } from "./types/UIProps"

export default defineAppConfig({
   icon: {
      size: "18px", // default <Icon> size applied
      class: "icon", // default <Icon> class applied
      mode: "svg" // default <Icon> mode applied
   },
   appName: "Kontext Copilot",
   apiBaseUrl: "http://localhost:8100",
   kontextCopilotUrl: "https://kontext.tech/copilot",
   kontextCopilotLinkedInUrl:
      "https://www.linkedin.com/company/kontext-technology",
   kontextCopilotRssUrl: "https://kontext.tech/api/flex/rss/250",
   settingKeys: {
      llmTemperture: "llm_temperature",
      llmEndpoint: "llm_endpoint",
      llmApiKey: "llm_api_key",
      llmDefaultModel: "llm_default_model",
      username: "general_username"
   },
   navItems: [
      {
         id: "home",
         to: "/",
         icon: "material-symbols:home-outline",
         text: "Home"
      },
      {
         id: "data",
         icon: "material-symbols:analytics-outline",
         text: "Data analytics",
         flat: true,
         children: [
            {
               id: "newChat",
               to: "/chat",
               icon: "material-symbols:chat-outline",
               text: "Chat"
            }
            // {
            //    id: "charts",
            //    to: "/charts",
            //    icon: "material-symbols:auto-graph",
            //    text: "Charts"
            // }
         ]
      },
      {
         id: "dataSources",
         to: "/data-sources",
         icon: "material-symbols:database-outline",
         text: "Data sources"
      },
      {
         id: "tools",
         icon: "material-symbols:tools-wrench-outline",
         text: "Tools",
         to: "/tools",
         flat: true
      },
      {
         id: "prompt",
         to: "/prompt-engineering",
         icon: "material-symbols:lightbulb-outline",
         text: "Prompt scratchboard",
         hidden: true
      },
      {
         id: "embedding",
         to: "/embedding-generator",
         icon: "material-symbols:transform",
         text: "Embedding generator",
         hidden: true
      },
      // { id: "llmflow", to: '/dashboards', icon: 'material-symbols:linked-services-outline', text: 'Workflows' },
      // { id: "knowledgebase", to: '/dashboards', icon: 'material-symbols:menu-book-outline', text: 'Knowledge base' },
      // { id: "dataSources", to: '/data-sources', icon: 'material-symbols:database-outline', text: 'Data sources' },

      // { id: "databoards", to: '/dashboards', icon: 'material-symbols:dashboard-customize-outline', text: 'Dashboards' },
      {
         id: "settings",
         to: "/settings",
         icon: "material-symbols:settings-outline",
         text: "Settings"
      }
   ] as NavItemProps[],
   tableClasses: "table table-striped table-hover table-sm"
})
