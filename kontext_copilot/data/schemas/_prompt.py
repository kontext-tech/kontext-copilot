from enum import Enum
from typing import List, Optional

from kontext_copilot.data.schemas._common import CamelAliasBaseModel


class PromptInfoModel(CamelAliasBaseModel):
    id: str
    name: Optional[str] = None
    system_defined: Optional[bool] = False


class PromptModel(PromptInfoModel):
    prompt: Optional[str] = None
    system_prompt: Optional[str] = None
    user_input: Optional[str] = None


class PromptListModel(CamelAliasBaseModel):
    prompts: List[PromptModel]


class QuestionTypes(Enum):
    """Type of question."""

    TEXT_TO_SQL = "text-to-sql"
    """The user is asking for returning a SQL statement."""

    TEXT_TO_CHART = "text-to-chart"
    """The user is asking for returning a chart."""

    TEXT_TO_TABLES = "text-to-tables"
    """The user is asking for returning a list of tables."""

    DEFAULT = "default"
    """The user is asking for other type of questions."""

    def get_details(self) -> str:
        """Get the details of the question type."""
        self.__doc__.strip()


class PromptTypes(Enum):
    """Type of prompt."""

    SYSTEM_PROMPT = "system_prompt"
    """System prompt."""

    QUESTION_TYPE_EXTRACTION = "question_type_extraction"
    """Question type extraction prompt."""

    TABLE_METADATA = "table_metadata"
    """Table metadata prompt."""

    TABLE_CREATE = "table_create"
    """Table creation prompt."""

    SCHEMA_TABLES = "schema_tables"
    """Schema with tables metadata prompt."""

    SCHEMA_TABLES_CREATE = "schema_tables_create"
    """Schema with tables creation prompt."""

    TEXT_TO_SQL = "text_to_sql"
    """Text to SQL prompt. Ask a question and returns a SQL statement."""

    TEXT_TO_TABLES = "text_to_tables"
    """Text to tables prompt. Ask a question and returns a list of tables."""

    DATA_TO_TEXT = "data_to_text"
    """Data to text prompt. Ask a question related to given data and returns a text."""

    DEFAULT = "default"
    """Default prompt."""


class PromptBuilder:
    """
    Prompt builder class.
    """

    def __init__(self):
        self.sb = []

    def append(self, line: str):
        """
        Add a line to the prompt.
        """
        self.sb.append(line)

    def add_new_line(self):
        """
        Add a new line to the prompt.
        """
        self.sb.append("")

    def build(self) -> str:
        """
        Build the prompt.
        """
        return "\n".join(self.sb)


class PromptNode:
    """Prompt node."""

    def __init__(
        self,
        prompt_type: PromptTypes,
        prompt_model: PromptModel,
        is_root: bool = False,
        children: List["PromptNode"] = [],
        **kwargs,
    ):
        self.prompt_type = prompt_type
        self.prompt_model = prompt_model
        self.is_root = is_root
        self.is_system_prompt = prompt_type == PromptTypes.SYSTEM_PROMPT
        self.children = children if children else []
        self.kwargs = kwargs

    def add_child(self, child: "PromptNode"):
        """Add a child to the node."""
        self.children.append(child)

    def add_children(self, children: List["PromptNode"]):
        """Add children to the node."""
        self.children.extend(children)

    def remove_child(self, child: "PromptNode"):
        """Remove a child from the node."""
        self.children.remove(child)

    def build_prompt(self, builder: PromptBuilder) -> str:
        """
        Get the prompt.

        Replace each key in format {{$key}} with the value from kwargs.
        """
        prompt_content = self.prompt_model.prompt
        system_prompt_content = self.prompt_model.system_prompt

        prompts = []
        if system_prompt_content:
            prompts.append(system_prompt_content)
        if prompt_content:
            prompts.append(prompt_content)
        prompt_str = "\n".join(prompts)

        # replace user input
        if self.prompt_model.user_input:
            prompt_str = prompt_str.replace("{{$input}}", self.prompt_model.user_input)

        for key, value in self.kwargs.items():
            if value:
                prompt_str = prompt_str.replace(f"{{{{${key}}}}}", value)

        builder.append(prompt_str)

        # Add children
        for child in self.children:
            child.build_prompt(builder, **self.kwargs)

        return builder.build()

    def get_prompt_str(self) -> str:
        """
        Get the prompt.
        """
        pb = PromptBuilder()
        return self.build_prompt(pb)


class PromptDocument:
    """Prompt document."""

    def __init__(self, root: PromptNode, **kwargs):
        self.root = root
        self.kwargs = kwargs
        self._builder = PromptBuilder()

    @staticmethod
    @classmethod
    def create(cls, **kwargs) -> "PromptDocument":
        """Create a prompt document."""
        root = PromptNode(
            prompt_type=PromptTypes.SYSTEM_PROMPT, prompt_model=PromptModel(), **kwargs
        )
        return cls(root, **kwargs)

    def add_params(self, **kwargs):
        """Add parameters to the prompt document."""
        self.kwargs.update(kwargs)

    def build_prompt(self) -> str:
        """
        Get the prompt.

        Replace each key in format {{$key}} with the value from kwargs.
        """

        return self.root.build_prompt(self._builder, **self.kwargs)
