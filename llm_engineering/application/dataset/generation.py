from abc import ABC, abstractmethod 

import tiktoken 
from langchain_core.exceptions import OutputParserException 
from langchain_core.language_models.fake import FakeListLLM 
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from loguru import logger 

from llm_engineering import domain
from llm_engineering.application import utils
from llm_engineering.domain.cleaned_documents import CleanedDocument
from llm_engineering.domain.dataset import DatasetType, TrainTestSplit
from llm_engineering.domain.prompt import GenerateDatasetSamplesPrompt, Prompt
from llm_engineering.domain.types import DataCategory
from llm_engineering.settings import settings 

from . import constants
from . import utils
from .output_parsers import ListPydanticOutputParser


# Based class to generate datasets, inherits from the abstract base class.
class DatasetGenerator(ABC):
    tokenizer = toktoken.encoding_for_model(settings.OPENAI_MODEL_ID)
    dataset_type = DatasetType | None = None

    system_prompt_template = """You are a helpful assistant who generates {dataset_format} based on the given context. \
        Provide your response in JSON format.
        """
    prompt_template_str: str | None = None

    @classmethod
    def get_system_prompt(cls) -> Prompt:
        # Ensure there is a dataset type, instruction or preference.
        assert cls.dataset_type is not None, "Dataset type must be set before calling get_system_prompt()"
        
        # Set the format to either instruction answer pairs or instruction answer triples
        dataset_format = (
            "instruction-answer pairs" if cls.dataset_type == DatasetType.INSTRUCTION else "instruction-answer triples"
        )
        # Set the input variables to be the dataset format.
        input_variables = {
            "dataset_format": dataset_format
        }
        # Set the system prompt to be based on the template.
        system_prompt = cls.system_prompt_template.format(**input_variables)
        
        # Return the full prompt.
        return Prompt(
            template = cls.system_prompt_template, 
            input_variables=input_variables, 
            content=system_prompt
        )

    # Method to get all prompts for the samples
    @classmethod 
    def get_prompts(cls, documents: list[CleanedDocument]) -> dict[DataCategory, list[GenerateDatasetSamplesPrompt]]:
        # Extract the substrings.
        documents = utils.extract_substrings(documents)

        # Empty dictionary for stored prompts
        grouped_prompts = {}
        # Group the documents by their data category
        grouped_cleaned_documents = CleanedDocument.group_by_category(documents)

        # Store the prompts based on their category in the grouped_prompts dictionary.
        for category, category_documents in grouped_cleaned_documents.items():
            category_prompts = [cls.get_prompt(document) for document in category_documents]
            grouped_prompts[category] = category_prompts

        return grouped_prompts
    
    # Mathod to get a single prompt for a given sample
    @classmethod
    def get_prompt(cls, document: CleanedDocument) -> GenerateDatasetSamplesPrompt:
        # Ensure the prompt_template is present.
        assert cls.prompt_template_str is not None, "Prompt template must be set before calling get_prompt()"

        # Pull the data category.
        data_category = document.get_category()

        prompt_template = PromptTemplate.from_template(
            template=cls.prompt_template_str, 
            template_format="jinja2",
        )

        # Set the extraction as the documents content.
        input_variables = {
            "extract": document.content
        }
        # Format based on content
        prompt = prompt_template.format(**input_variables)
        # Tokenize the content.
        prompt_tokens = cls.tokenizer.encode(prompt)
        # If we go past the max token length then we only pull tokens up to the maximum length.
        if len(prompt_tokens) > settings.OPENAI_MAX_TOKEN_WINDOW:
            prompt_tokens = prompt_tokens[: settings.OPENAI_MAX_TOKEN_WINDOW]
            prompt = cls.tokenizer.decode(prompt_tokens)
        
        # Finalize the prompt 
        prompt = GenerateDatasetSamplesPrompt(
            template=prompt_template.template, 
            input_variables=input_variables, 
            content=prompt, 
            num_tokens=len(prompt_tokens),
            data_category=data_category, 
            document=document,
        )

        return prompt
    
    # Method to generate prompts
    @classmethod
    def generate(
        cls, 
        prompts: dict[DataCategory, list[GenerateDatasetSamplesPrompt]], 
        test_size: float = 0.2,
        mock: bool = False,
    ) -> TrainTestSplit:
        assert cls.dataset_type is not None, "Dataset type must be set before calling generate()"

        # Internal function to push samples into langchain to get the system and human messages.
        def _to_langchain(
                prompt: GenerateDatasetSamplesPrompt
        )-> list[BaseMessage]:
            messages = [
                SystemMessage(content=cls.get_system_prompt().content),
                HumanMessage(content=prompt.content),
            ]

            return messages

        if mock:
            llm = FakeListLLM(responses=[constants.get_mocked_response(cls.dataset_type)])

