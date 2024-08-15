import json
import os
from functools import lru_cache
from typing import List

from sqlalchemy import Table

from kontext_copilot.data.schemas import (
    DataSourceModel,
    PromptBuilder,
    PromptListModel,
    PromptModel,
    PromptNode,
    PromptTypes,
)
from kontext_copilot.utils import get_logger

# prompt template file path
PROMPT_TEMPLATE_FILE = "./prompts.json"


@lru_cache(maxsize=None)
def read_prompt_file_with_cache(file_path):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_path))
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()


logger = get_logger()


class PromptFactory:
    """
    Factory class for creating prompts.
    """

    @staticmethod
    def create_default_system_prompt(**kwargs) -> PromptNode:
        logger.info("Creating default system prompt")
        prompt_model = PromptFactory.get_prompt_template_by_id("system-prompt-default")
        return PromptNode(
            prompt_type=PromptTypes.SYSTEM_PROMPT,
            prompt_model=prompt_model,
        )

    @staticmethod
    def create_system_prompt(
        data_source: DataSourceModel, tables: List[Table], **kwargs
    ) -> PromptNode:

        logger.info("Creating system prompt for data source: %s", data_source.name)

        prompt_model = PromptFactory.get_prompt_template_by_id(
            "system-prompt-da-metadata"
        )

        logger.debug("Prompt template: %s", prompt_model)

        # Get the tables metadata
        tables_metadata = []
        for table in tables:
            tables_metadata.append(
                PromptFactory.create_table_metadata_prompt(table).get_prompt_str()
            )
        tables_metadata_str = "\n".join(tables_metadata)

        # Add params for the prompt
        params = {}
        params.update(kwargs)
        params["tables_metadata"] = tables_metadata_str

        node = PromptNode(
            prompt_type=PromptTypes.SYSTEM_PROMPT,
            prompt_model=prompt_model,
            **params,
        )

        return node

    @staticmethod
    def create_question_type_extraction_prompt() -> PromptNode:
        """
        Create a prompt for the question type extraction.
        """

        pb = PromptBuilder()
        pb.append("## Question Type Extraction")
        pb.add_new_line()
        pb.append("### Extracting the question type from the given text.")
        pb.add_new_line()
        pb.append("#### Question:")
        pb.add_new_line()
        pb.append("What is the question type?")
        pb.add_new_line()
        pb.append("#### Example:")
        pb.add_new_line()
        pb.append("Given the text: 'What is the capital of France?'")
        pb.add_new_line()
        pb.append("The question type is: 'Location'")
        pb.add_new_line()

        prompt_model = PromptModel(prompt=pb.build())

        return PromptNode(
            prompt_type=PromptTypes.QUESTION_TYPE_EXTRACTION, prompt_model=prompt_model
        )

    @staticmethod
    def create_table_metadata_prompt(table: Table) -> PromptNode:
        """
        Create a prompt for the table.
        """

        pb = PromptBuilder()
        pb.append(f"## Table: {table.fullname}")
        pb.add_new_line()
        pb.append("### Columns:")
        pb.add_new_line()
        for column in table.columns:
            pb.append(
                f"- {column.name}: {column.type} ({'nullable' if column.nullable else 'not nullable'})"
            )

        prompt_model = PromptModel(
            prompt=pb.build(), id=f"table-metadata-{table.fullname}"
        )

        return PromptNode(
            prompt_type=PromptTypes.TABLE_METADATA, prompt_model=prompt_model
        )

    @staticmethod
    def load_prompts_from_json() -> PromptListModel:
        """
        Load prompts from a JSON file and return a Prompts object.

        Returns:
            Prompts: A Prompts object containing the loaded prompts.
        """

        abs_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), PROMPT_TEMPLATE_FILE)
        )
        with open(abs_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        model_list = PromptListModel(**data)

        # Check prompt and system prompt:
        # if value is a path (for example, "./prompts/sentiment-analysis.md"),
        # get the content from the file and replace the value
        for prompt in model_list.prompts:
            prompt_content = prompt.prompt
            sys_prompt_content = prompt.system_prompt
            if prompt_content is not None and prompt_content.startswith("./prompts/"):
                logger.info(f"Read prompt from file: {prompt_content}")
                prompt.prompt = read_prompt_file_with_cache(prompt_content)
            if sys_prompt_content is not None and sys_prompt_content.startswith(
                "./prompts/"
            ):
                logger.info(f"Read prompt from file: {sys_prompt_content}")
                prompt.system_prompt = read_prompt_file_with_cache(sys_prompt_content)
        return model_list

    @staticmethod
    def get_prompt_template_by_id(template_id: str) -> PromptModel:
        """
        Get a prompt template by id.

        Args:
            template_id (str): The id of the prompt template.

        Returns:
            PromptModel: The prompt template.
        """
        prompts = PromptFactory.load_prompts_from_json()

        # find prompt by id
        prompt = next((p for p in prompts.prompts if p.id == template_id), None)

        return prompt
