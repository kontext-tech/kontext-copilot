import type { ChatResponse, Message } from "ollama/browser"

export enum ChatRoles {
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

export interface LlmModelResponse {
   name: string
   modifiedAt: Date
   size: number
   digest: string
   details: LlmModelDetails
   expiresAt: Date
   sizeVram: number
}

export interface LlmModelDetails {
   parentModel: string
   format: string
   family: string
   families: string[]
   parameterSize: string
   quantizationLevel: string
}

export interface LlmModelListResponse {
   models: LlmModelResponse[]
}

export interface LlmChatMessage extends Message {
   id?: number
   content: string
   role: ChatRoles
   generating?: boolean
   isStreaming?: boolean
   isError?: boolean
   isSystemPrompt?: boolean
   sqlStatements?: string[]
}

export interface LlmChatResponse extends ChatResponse {
   message: LlmChatMessage
}

export interface LlmToolbarOptions {
   streaming: boolean
   format: "json" | ""
   model?: string
}

export interface LlmClientState {
   history: LlmChatMessage[]
   generating: boolean
   error: string | null
   currentResponse: LlmChatMessage
   abort: boolean
   messageIndex: number
   session?: SessionInitResponseModel
}

export interface SettingsModel {
   llmDefaultModel: string
   llmTemperature: number
   llmApiKey: string | null
   llmEndpoint: string
   llmOllamaEndpoint: string
   generalTheme: ThemeName
   generalUsername: string
   llmTopP: number
   llmTopK: number
   llmSeed: number
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
   systemPrompt?: string
   userInput: string
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
   connStr: string
}

// Create model excludes auto-generated fields like 'id'
export interface DataSourceCreateModel {
   name?: string
   description?: string // Made optional by adding '?'
   type?: DataSourceType | null
   connStr?: string
}

// Update model makes all fields optional
export interface DataSourceUpdateModel {
   name?: string
   description?: string
   type?: DataSourceType
   connStr?: string
}

export interface SchemaTablesModel {
   schemaName: string | null
   tables: string[]
}

export interface ColumnInfoModel {
   name: string
   primaryKey: boolean
   index?: boolean
   unique?: boolean
   dataType: string
   nullable: boolean
   default?: string
   autoincrement?: boolean
   comment?: string
}

export interface DataProviderInfoModel extends DataSourceModel {
   supportsSchema: boolean
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

export interface SessionInitRequestModel {
   model: string
   dataSourceId: number
   tables?: string[]
   schemaName?: string
   sessionId?: number
}

export interface SessionInitResponseModel {
   systemPrompt: string
   sessionId: number
   title?: string
   model?: string
   dataSourceId: number
   tables?: string[]
   schemaName?: string
}

export interface RunSqlRequestModel {
   dataSourceId: number
   sql: string
   schemaName?: string
   maxRecords?: number
}

export interface ErrorResponseModel {
   error: string
   detail?: string
}
