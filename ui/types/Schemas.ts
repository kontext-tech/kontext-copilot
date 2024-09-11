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

export interface LlmChatMessage {
   content: string
   role: ChatRoles
}

export enum ActionTypes {
   RUN_SQL = "run_sql",
   COPY_SQL = "copy_sql",
   SQL_TO_PYTHON = "sql_to_python",
   SQL_TO_PYSPARK = "sql_to_pyspark",
   FIX_SQL_ERRORS = "fix_sql_errors",
   RECOMMEND_CHARTS = "recommend_charts"
}

export interface ActionsModel {
   actions: ActionTypes[]
   data?: { [key: string]: unknown }
}

export enum ActionsDataKeys {
   SQL_LIST = "sql",
   SQL_TEXT = "sqlText",
   SQL_TO_PYTHON_PROMPT = "sqlToPythonPrompt",
   SQL_TO_PYSPARK_PROMPT = "sqlToPysparkPrompt",
   FIX_SQL_ERRORS_PROMPT = "fixSqlErrorsPrompt",
   RECOMMENDED_CHARTS = "recommendedCharts"
}

export interface CopilotSessionMessage extends LlmChatMessage {
   id?: number
   sessionId?: number
   model?: string
   generating?: boolean
   isStreaming?: boolean
   isError?: boolean
   isSystemPrompt?: boolean
   copilotGenerated?: boolean
   done?: boolean
   doneReason?: string
   totalDuration?: number
   loadDuration?: number
   promptEvalCount?: number
   promptEvalDuration?: number
   evalCount?: number
   evalDuration?: number
   actions?: ActionsModel
}

export interface LlmToolbarOptions {
   streaming: boolean
   format: "json" | ""
   model?: string
}

export interface CopilotState {
   messages: CopilotSessionMessage[]
   currentMessage?: CopilotSessionMessage
   abort: boolean
   session?: SessionInitResponseModel
   // For overall status incl. embeddings and other generation
   generating?: boolean
   generatedContent?: string
   generatedEmbeddings?: number[]
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
   SQLite = "SQLite",
   DuckDB = "DuckDB",
   PostgreSQL = "PostgreSQL",
   // MySQL = "MySQL",
   SQLServer = "SQLServer",
   // Oracle = "Oracle",
   // MongoDB = "MongoDB",
   // Redis = "Redis",
   CSV = "CSV",
   Parquet = "Parquet"
}

export interface DataSourceModel {
   id: number // Optional in TypeScript
   name: string
   description?: string // Optional in TypeScript
   type: DataSourceType
   connStr: string
}

export interface DataSourceWrapModel {
   model: DataSourceModel | null
   isLoading: boolean
   loaded: boolean
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
   model: DataProviderInfoModel | null
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
   dataSourceId?: number
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
   sessionId?: number
   parentMessageId?: number
}

export interface ChatRequestModel {
   model: string
   messages?: LlmChatMessage[]
   stream?: boolean
   format: "" | "json"
   options?: Partial<LLmOptions>
   keepAlive?: string | number
   sessionId?: number
}

export interface AddUserMessageRequestModel {
   sessionId?: number
   content: string
   model: string
}

export interface EmbeddingsRequestModel {
   model: string
   prompt: string
   keepAlive?: string | number
   options?: Partial<LLmOptions>
}

export interface EmbeddingsResponseModel {
   embedding: number[]
}

export interface GenerateRequestModel {
   model: string
   prompt: string
   suffix?: string
   system?: string
   template?: string
   context?: number[]
   stream?: boolean
   raw?: boolean
   format?: string
   images?: Uint8Array[] | string[]
   keepAlive?: string | number
   options?: Partial<LLmOptions>
}

export interface GenerateResponseModel {
   model: string
   created_at: Date
   response: string
   done: boolean
   doneReasons?: string
   context?: number[]
   totalDuration?: number
   loadDuration?: number
   promptEvalCount?: number
   promptEvalDuration?: number
   evalCount?: number
   evalDuration?: number
}

export interface LLmOptions {
   numa: boolean
   num_ctx: number
   num_batch: number
   num_gpu: number
   main_gpu: number
   low_vram: boolean
   f16_kv: boolean
   logits_all: boolean
   vocab_only: boolean
   use_mmap: boolean
   use_mlock: boolean
   embedding_only: boolean
   num_thread: number
   num_keep: number
   seed: number
   num_predict: number
   top_k: number
   top_p: number
   tfs_z: number
   typical_p: number
   repeat_last_n: number
   temperature: number
   repeat_penalty: number
   presence_penalty: number
   frequency_penalty: number
   mirostat: number
   mirostat_tau: number
   mirostat_eta: number
   penalize_newline: boolean
   stop: string[]
}

export interface ErrorResponseModel {
   error: string
   detail?: string
}

export enum ChatTypes {
   GENGERAL_CHAT = "general_chat",
   CHAT_TO_DATA = "chat_to_data"
}

export interface ChatTypeSelectorModel {
   chatType?: ChatTypes
   modalOpen: boolean
   show: boolean
}

export interface ChatStateModel {
   sessionTitle: string
   chatTypeSelector: ChatTypeSelectorModel
   schemaSelector: SchemaSelectorModel
   sql: string
   dataSource: DataSourceWrapModel
   dataProvider: DataProviderInfoWrapModel
   llmOptions: LlmToolbarOptions
}

export interface SchemaSelectorModel {
   schema?: string
   tables: string[]
   selectAll: boolean
}

export interface RunSqlModalModel {
   open: boolean
   sql: string
   maxRecords?: number
}

export enum ChartTypes {
   PIE = "pie",
   BAR = "bar",
   LINE = "line"
}

export enum AggregateTypes {
   SUM = "sum",
   AVG = "avg",
   COUNT = "count",
   MAX = "max",
   MIN = "min"
}

export interface ChartModel {
   chartType: ChartTypes
   aggregateType?: AggregateTypes
}

export interface PieChartModel extends ChartModel {
   chartType: ChartTypes.PIE
   title?: string
   dataColumn: string
   labelColumn?: string
}

export interface BarChartModel extends ChartModel {
   chartType: ChartTypes.BAR
   title?: string
   xTitle?: string
   yTitle?: string
   xDataColumn: string
   xLabelColumn?: string
   yDataColumn: string
   yLabelColumn?: string
}

export interface LineChartModel extends ChartModel {
   chartType: ChartTypes.LINE
   title?: string
   xTitle?: string
   yTitle?: string
   xDataColumn: string
   xLabelColumn?: string
   yDataColumn: string
   yLabelColumn?: string
}

export interface ChartListModel {
   charts: (PieChartModel | BarChartModel | LineChartModel)[]
   cached: boolean
   cachedTableName?: string
}

export interface ChartDataModel {
   labels: string[]
   datasets: { [key: string]: unknown }[]
}

export interface ChartOptionsModel {
   plugins?: { [key: string]: unknown }
}

export interface ChartDataRequestModel {
   chart: PieChartModel | BarChartModel | LineChartModel
   cached?: boolean
   cachedTableName?: string
   dataSourceId: number
   schemaName?: string
   sessionId?: number
   messageId?: number
}

export interface ChartDataResponseModel {
   data: ChartDataModel
   type: ChartTypes
   options?: ChartOptionsModel
}
