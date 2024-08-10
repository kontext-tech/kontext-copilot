from typing import Iterator, Optional
from kontext_copilot.copilot._prompt_factory import PromptFactory as pf
from kontext_copilot.copilot._session import Session
from kontext_copilot.services import (
    get_data_sources_service,
    get_db_engine,
    DataProviderService,
)
from kontext_copilot.utils import get_logger


class Planner:
    def __init__(self):
        self._logger = get_logger()
        self._engine = get_db_engine()
        self._ds_service = get_data_sources_service(self._engine)

    def init_session(
        self, data_source_id: int, tables: Optional[list[str]], schema: Optional[str]
    ) -> Session:
        """
        Initialise session for the copilot
        """
        self._logger.info("Initialising session for data source: %s", data_source_id)
        self.session = Session(data_source_id, tables, schema)
        self._logger.info("Session initialised")
        return self.session

    def _check_session(self):
        if not self.session:
            raise ValueError("Session not initialised")

    def _get_provider(self, data_source_id: int):
        """
        Get the data provider based on the data source id.
        """
        try:
            self._logger.info(
                f"Retrieving data provider for data source id: {data_source_id}"
            )
            source = self._ds_service.get_data_source(data_source_id)
            provider = DataProviderService.get_data_provider(source)
            return provider
        except Exception as e:
            self._logger.error(
                f"Error retrieving data provider (#{data_source_id}): {e}"
            )
            raise e

    def run_sql(self, sql: str, max_records: int = 10) -> Iterator[str]:
        """
        Run SQL
        """
        self._check_session()
        self._logger.debug("Running SQL: %s", sql)
        yield "Sure thing!\n"
        yield "\n***SQL:***\n"
        yield f"```sql\n{sql}\n```\n"

        provider = self._get_provider(self.session.data_source_id)
        result = provider.run_sql(sql)
        total_records = len(result)
        yield "\n***Results:***\n\n"
        if total_records == 0:
            yield "0 records returned.\n"
        else:
            keys = result[0].keys()
            if total_records > max_records:
                result = result[:max_records]
                yield f"(showing first **{max_records}** records out of **{total_records}**).\n"

            yield "|"
            for col in keys:
                yield f"{col}|"
            yield "\n"
            yield "|"
            for _ in keys:
                yield "---|"
            yield "\n"
            for row in result:
                yield "|"
                for col in row.values():
                    yield f"{col}|"
                yield "\n"

    def get_system_prompt(self):
        """
        Get system prompt
        """
        self._check_session()

        prompt = self.session.get_system_prompt()

        self._logger.debug("System prompt: %s", prompt)

        return prompt.get_prompt_str()
