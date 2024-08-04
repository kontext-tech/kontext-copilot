import type { Message } from "ollama/browser"

export enum ChatRole {
   USER = "user",
   ASSISTANT = "assistant",
   SYSTEM = "system"
}

export interface ThemeNames {
   dark: unknown
   light: unknown
   auto: unknown
}

export type ThemeName = keyof ThemeNames

export interface ThemeConfigItem {
   key: ThemeName
   iconName: string
   name: string
}

export interface ChatMessage extends Message {
   id?: number
   content: string
   role: ChatRole
   generating?: boolean
   isStreaming?: boolean
   isError?: boolean
}

export interface LlmToolbarOptions {
   streaming: boolean
   format: "json" | ""
   model?: string
}

export interface LlmClientState {
   history: ChatMessage[]
   generating: boolean
   error: string | null
   currentResponse: ChatMessage
   abort: boolean
   messageIndex: number
}

export interface SettingsModel {
   llm_default_model: string
   llm_temperature: number
   llm_api_key: string | null
   llm_endpoint: string
   llm_ollama_endpoint: string
   general_theme: ThemeName
   general_username: string
   llm_top_p: number
   llm_top_k: number
   llm_seed: number
}

export interface SettingsModelWrapper {
   settings: SettingsModel
   isLoading: boolean
   loaded: boolean
   error: string | null
}

export interface PromptInfoModel {
   id: string
   name: string
}

export interface PromptModel extends PromptInfoModel {
   prompt: string
   system_prompt?: string
   user_input: string
}

export interface PromptListModel {
   prompts: PromptModel[]
}

export enum DataSourceType {
   SQLite = "SQLite"
   // DuckDB = "DuckDB",
   // PostgreSQL = "PostgreSQL",
   // MySQL = "MySQL",
   // SQLServer = "SQLServer",
   // Oracle = "Oracle",
   // MongoDB = "MongoDB",
   // Redis = "Redis",
}

export interface DataSourceModel {
   id: number // Optional in TypeScript
   name: string
   description?: string // Optional in TypeScript
   type: DataSourceType
   conn_str: string
}

// Create model excludes auto-generated fields like 'id'
export interface DataSourceCreateModel {
   name?: string
   description?: string // Made optional by adding '?'
   type?: DataSourceType | null
   conn_str?: string
}

// Update model makes all fields optional
export interface DataSourceUpdateModel {
   name?: string
   description?: string
   type?: DataSourceType
   conn_str?: string
}

export interface SchemaTablesModel {
   schema: string | null
   tables: string[]
}

export interface ColumnInfoModel {
   name: string
   primary_key: boolean
   index?: boolean
   unique?: boolean
   data_type: string
   nullable: boolean
   default?: string
   autoincrement?: boolean
   comment?: string
}

export interface DataProviderInfoModel extends DataSourceModel {
   supports_schema: boolean
   metadata: SchemaTablesModel[]
}

export interface DataProviderInfoWrapModel {
   provider: DataProviderInfoModel | null
   isLoading: boolean
}

export interface SqlStatementModel {
   sql: string
}

export interface SqlStatementType {
   CREATE: unknown
   SELECT: unknown
}

export interface SqlRunResultModel {
   success: boolean
   message?: string
   data: Array<object>
}

export type SqlType = keyof SqlStatementType

export interface CopilotSessionRequestModel {
   model: string
   data_source_id: number
   tables?: string[]
   schema?: string
}

export interface CopilotSessionResponseModel {
   prompt: string
}
