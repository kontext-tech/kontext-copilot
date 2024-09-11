## v0.6.1 (2024-09-11)

### Fix

- sanitize html using vue dom purify package. (#55)

## v0.6.0 (2024-09-11)

### Feat

- added file sources for CSV and parquet files. (#53)

## v0.5.0 (2024-09-10)

### Feat

- added env var KONTEXT_COPILOT_DEFAULT_SYS_PROMPT to set differe… (#50)

## v0.4.0 (2024-09-09)

### Feat

- added support for PostgreSQL using psycopg 3

## v0.3.2 (2024-09-09)

### Fix

- duckdb.duckdb.CatalogException: Catalog Error: Scalar Function with name sum does not exist!

## v0.3.1 (2024-09-08)

### Fix

- add workflow_dispatch for version bump flow
-  commitizen cz bump triggers for other workflows: https://commitizen-tools.github.io/commitizen/tutorials/github_actions/

## v0.3.0 (2024-09-08)

## 0.2.0 (2024-09-08)

### Feat

- added Chinook sample db into package and ensure it is added as source when app starts
- added alerts for chat-to-data and execute sql actions.
- added splash loading screen
- added SQL Server support.
- added duckdb support
- moved pie chart recommendation to front.
- added charts recommendation function in both backend and frontend.
- cached query run result in duckdb.
- started to add recommended chart types to run sql result.
- added new chat button when modal is closed.
- removed links from home page
- added links to project site and linkin
- added suggestion questions to ask link button.
- added fix error action.
- not remove current state until chat type seleted.
- added new chat link to secondary header
- increased the size of sql text input.
- added user input into session message table.
- added text to show length of embeddings
- added to python code action; fixed popover tooltip for copy button.
- added copy sql action.
- implemented action to run sql code
- implemented extract sql tool
- add session and message id to chat message response
- added session id to run sql call
- added mechanism to reuse session id for the same model and data source
- enhanced init session to return a session id number.
- add model column to session
- added session and session message models in database.
- redesigned layout and moved llm settings button to top nav.
- updated layout to add footer user info
- hide icon if it is system message
- changed run sql result to system message only.
- Added generic error handling
- added dekat when running sql
- enhanced run sql feature.
- optimize
- started to add copilot core logic - system prompt; refactored prompt templates.
- added error catch for chat
- added abort button for streaming chat.
- added load in progress.
- Added chat func to chat to data window
- Added auto-select property to auto select first source
- Added refresh button to data source provider
- implemented data query tab
- Added SELECT script and copy to clipboard
- Added components to display data source schema and to show create table script and sample script.
- Added APIs to query tables' schema and data.
- Added data provider to interact with data sources.
- Added selector of data source.
- Added function to delete data source.
- Add component to edit data source.
- Added data source list page and form component to add new data source.
- Added API handlers for data sources
- Added service to operate on data sources; renamed pydantic models.
- Added data source table into sql model.
- turn off Nuxt dev tool.
- Replaced usebootstrap with @bootstrap-vue-next/nuxt
- Make model selector simpler
- Make settings singleton.
- Added embeddings generator.
- Added generate API and prompt scratchboard to test prompts.
- Remove packaged not used.
- Added more LLM settings.
- Updated settings to use APIs
- added api services for settings; added pydantic for schemas.
- Added sqlalchemy and alembic for operating with database
- Changed client to use fastapi instead ollama call - support chat and list APIs only for now .

### Fix

- session init issues when switching chat types.
- session initiated twice problem.
- increase category unique threshold to 256
- scroll issue and error when there is null in categorical column
- chart render bug
- only recommend categorical bars when unique values <= 10
- bug when column has spaces
- reset llm format and streaming options
- chat selector session switch issue.
- a few issues
- only show suggestion button for chat to data window
- bug of getting env name.
- reset issues of using Object.assign as it is shallow copy not deep.
- flushing of system prompt message
- init session not triggered issue
- long lines in code
- not showing table/schema selection for the first load.
- non-streaming generation.
- title not changing for initial session.
- empty string returned in tables list.
- source selector change to cascade to schema ones using v-model.
- table breaking message card
- format.
- logging format; added color logging
- options of llm chat is not reactive.
- fixed settings data type for numberic values
- bug of loading int values for float type settings attribute
- fixed source edit form issue and added copy button
- watch when tables change (use deep watch).
- Make model list retrival singleton.
- remove console.log
- error in generating method; changed service name
- [nuxt] Your project has layouts but the `<NuxtLayout />` component has not been used.
- build script
- lint errors.
- eslint
- Errors of decompose props (make them not reactive)
- make model selection global.
- always show modal.
- insert and other DML statements execution.
- run sql function to allow DML too.
- copy message and text
- page title composable
- Theme toggle sync issue
- Ensure api endpoints are called for LLM APIs.

### Refactor

- renamed copilot core classes
- moved utils to one tools page.
- merge chat to data and general chat to one page.
- reuse main window for general chat too.
- actionsmodel to share data attributes across multiple action types.
- chat input box
- changed generate and embeddings to camel case for client models except for options.
- moved all prompt related to schema module.
- improve performance by only commit message to db at the end.
- merged llm api endpoints to copilot one.
- changed from direct api call to llm chat tool; refactored models to make it consistent with session message model.
- changed from direct api call to llm chat tool; refactored models to make it consistent with session message model.
- client service and message card.
- added message id and others; fixed response.
- added tool concept to handle copilot requests.
- upgraded npm packages to the latest
- renamed llmclientservice to copilotclientservice
- replaced model list response models; added more details to model selector
- changed all models to pydantic and typescript models to use camel case.
- moved run-sql to server side using streaming api
- moved components to chat sub folder
- added toolbar for llm settings with tooggles
- move embeddings to LlmClientService; added util function to get service easily.
- prompt engineering to use LLmClientService.
- chat services to be one to easy maintainence
- move services setup to a composable to simplify app.vue
- Renamed injected service names
- services to use dependency injection.
- chart message component
- renamed kontext_ai to kontext_copilot
- data source creation
- Simplify sidebar nav
- changed refresh icon to a button
- simplify
- simplify theme toggle and schema display components.
- from data providers to services
- renamed data source components path
- Simplified component names by using sub folders.
- Renamed client-app to ui
