import axios from 'axios'
import type { Settings, PromptInfo, Prompt, DataSourceModel, DataSourceCreateModel, DataSourceUpdateModel, ColumnInfoModel, DataProviderInfoModel, SqlStatementModel, SqlRunResultModel } from '~/types/Schemas'

const getBaseUrl = (apiBaseUrl: string) => {
  return `${apiBaseUrl}/api`
}

axios.defaults.headers.post['Content-Type'] = 'application/json'

export class SettingsService {

  constructor(apiBaseUrl: string) {
    axios.defaults.baseURL = getBaseUrl(apiBaseUrl)
  }

  async getSettings(): Promise<Settings> {
    const response = await axios.get('/settings/')
    return response.data
  }

  async updateSetting(key: string, value: string | number): Promise<boolean> {
    const response = await axios.post('/settings/', {
      key,
      value: (typeof value === 'number') ? value.toString() : value,
    })
    if (response.status === 200) {
      return true
    }
    return false
  }
}

export class PromptsService {
  constructor(apiBaseUrl: string) {
    axios.defaults.baseURL = getBaseUrl(apiBaseUrl)
  }

  async getPromptTemplates(): Promise<PromptInfo[]> {
    const response = await axios.get('/prompts/templates')
    return response.data
  }

  async getPromptTemplate(template_id: string): Promise<Prompt> {
    const response = await axios.get(`/prompts/templates/${template_id}`)
    return response.data
  }

}

export class DataSourcesService {
  constructor(apiBaseUrl: string) {
    axios.defaults.baseURL = getBaseUrl(apiBaseUrl)
  }

  async getDataSources(): Promise<DataSourceModel[]> {
    const response = await axios.get('/data-sources/')
    return response.data
  }

  async getDataSource(id: number): Promise<DataSourceModel> {
    const response = await axios.get(`/data-sources/${id}`)
    return response.data
  }

  async createDataSource(data: DataSourceCreateModel): Promise<DataSourceModel> {
    const response = await axios.post('/data-sources/', data)
    return response.data
  }

  async updateDataSource(id: number, data: DataSourceUpdateModel): Promise<DataSourceModel> {
    const response = await axios.put(`/data-sources/${id}`, data)
    return response.data
  }

  async deleteDataSource(id: number): Promise<DataSourceModel> {
    const response = await axios.delete(`/data-sources/${id}`)
    return response.data
  }
}

export class DataProviderService {
  constructor(apiBaseUrl: string) {
    axios.defaults.baseURL = getBaseUrl(apiBaseUrl)
  }

  async getDataProviderInfo(dataSourceId: number): Promise<DataProviderInfoModel> {
    const response = await axios.get<DataProviderInfoModel>(`/data-providers/${dataSourceId}`)
    return response.data
  }

  async getColumns(dataSourceId: number, table: string, schema?: string): Promise<ColumnInfoModel[]> {
    const params = { table, schema }
    const response = await axios.get<ColumnInfoModel[]>(`/data-providers/${dataSourceId}/columns`, { params })
    return response.data
  }

  async getTableSamples(dataSourceId: number, table: string, schema?: string, recordCount: number = 10): Promise<object[]> {
    const params = { table, schema, record_count: recordCount }
    const response = await axios.get<object[]>(`/data-providers/${dataSourceId}/table-samples`, { params })
    return response.data
  }

  async getTableCreationSQL(dataSourceId: number, table: string, schema?: string): Promise<SqlStatementModel> {
    const params = { table, schema }
    const response = await axios.get<SqlStatementModel>(`/data-providers/${dataSourceId}/table-creation-sql`, { params })
    return response.data
  }

  async getTableSelectSQL(dataSourceId: number, table: string, schema?: string): Promise<SqlStatementModel> {
    const params = { table, schema }
    const response = await axios.get<SqlStatementModel>(`/data-providers/${dataSourceId}/table-select-sql`, { params })
    return response.data
  }

  async runSql(dataSourceId: number, sql: string, schema?: string, recordCount?: number): Promise<SqlRunResultModel> {
    const params = { sql, schema, record_count: recordCount }
    const response = await axios.post<SqlRunResultModel>(`/data-providers/${dataSourceId}/run-sql`, params)
    return response.data
  }
}
