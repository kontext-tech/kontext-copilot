import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Our 4-bit configuration to load the LLM with less GPU memory
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="uint8")
quantization_config = bnb_config if torch.cuda.is_available() else None
device_map = "auto" if torch.cuda.is_available() else None

# default model path
current_dir = os.path.dirname(__file__)
MODEL_PATH = os.path.join(current_dir, "TinyLlama")
MODEL_PATH = os.path.abspath(MODEL_PATH)

MODEL_FILE = "TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"


class LLMFactory:
    __llm_instance = None
    __tokenizer_instance = None

    def __init__(self):
        if not LLMFactory.__llm_instance:
            LLMFactory.__llm_instance = AutoModelForCausalLM.from_pretrained(
                MODEL_PATH,
                gguf_file=MODEL_FILE,
                ggml_type="Q4_K",
                local_files_only=True,
                quantization_config=quantization_config,
                device_map=device_map,
            )
        if not LLMFactory.__tokenizer_instance:  # Initialize tokenizer singleton
            LLMFactory.__tokenizer_instance = AutoTokenizer.from_pretrained(
                MODEL_PATH,
                gguf_file=MODEL_FILE,
                ggml_type="Q4_K",
                local_files_only=True,
                quantization_config=quantization_config,
                device_map=device_map,
            )

    @staticmethod
    def get_llm():
        if not LLMFactory.__llm_instance:
            LLMFactory()
        return LLMFactory.__llm_instance

    @staticmethod
    def get_tokenizer():
        if not LLMFactory.__tokenizer_instance:
            LLMFactory()
        return LLMFactory.__tokenizer_instance
