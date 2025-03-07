
import os
from dotenv import load_dotenv
from llama_index.multi_modal_llms.huggingface import HuggingFaceMultiModal
from typing import Any, Dict, Sequence, Union

from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from transformers import (
    AutoProcessor,
    AutoModelForCausalLM,
    AutoConfig,
    Qwen2VLForConditionalGeneration,
    PaliGemmaForConditionalGeneration,
    MllamaForConditionalGeneration,
)
load_dotenv()

from gradio_client import Client, handle_file

from llama_index.multi_modal_llms.gemini import GeminiMultiModal
class Model:

    GEMINI_1_5_PRO = GeminiMultiModal(
            model_name="models/gemini-1.5-pro",
            api_key=os.environ.get("GEMINI_API_KEY"),
            temperature=0
        )
    GPT_4_O = OpenAIMultiModal(model="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY"), image_detail="high", temperature=0)

    # TODO https://huggingface.co/CohereForAI/aya-vision-32b

    """ The following code runs the model locally, and is very slow on my machine, though probably usable with a GPU"""
    # class CustomHuggingFaceMultiModal(HuggingFaceMultiModal):
    #     def __init__(self, **kwargs: Any) -> None:
    #         """
    #         Initializes the HuggingFace multi-modal model and processor based on the provided configuration.
    #         """
    #         super().__init__(**kwargs)
    #         try:
    #             Load model configuration
                # self._config = AutoConfig.from_pretrained(
                #     self.model_name, trust_remote_code=True
                # )
                # architecture = self._config.architectures[0]
                # AutoModelClass = AutoModelForCausalLM  # Default model class
                #
                # Special cases for specific model architectures
                # if "Qwen2VLForConditionalGeneration" in architecture:
                #     AutoModelClass = Qwen2VLForConditionalGeneration
                # if "PaliGemmaForConditionalGeneration" in architecture:
                #     AutoModelClass = PaliGemmaForConditionalGeneration
                # if "MllamaForConditionalGeneration" in architecture:
                #     AutoModelClass = MllamaForConditionalGeneration
                #
                # Load the model based on the architecture
                # self._model = AutoModelClass.from_pretrained(
                #     self.model_name,
                #     device_map='cpu',
                #     torch_dtype=self.torch_dtype,
                #     trust_remote_code=self.trust_remote_code,
                #     low_cpu_mem_usage=True,
                #     **self.additional_kwargs,
                # )
                # from accelerate import disk_offload
                # disk_offload(model=self._model, offload_dir="offload")
                # Load the processor (for handling text and image inputs)
                # self._processor = AutoProcessor.from_pretrained(
                #     self.model_name, trust_remote_code=self.trust_remote_code
                # )
            # except Exception as e:
            #     raise ValueError(f"Failed to initialize the model and processor: {e!s}")
    # PALIGEMMA = CustomHuggingFaceMultiModal(model_name="agentsea/paligemma-3b-ft-waveui-896").from_model_name("agentsea/paligemma-3b-ft-waveui-896")
    class PaligemmaApi:
        def __init__(self):
            self.client = Client("agentsea/paligemma-waveui", hf_token=os.getenv("HUGGINGFACE_TOKEN"))

        def process(self, query, image_route="screenshot.png"):
            result = self.client.predict(
                input_image=handle_file(image_route),
                input_text=query,
                model_choice="paligemma-3b-ft-waveui-896",
                api_name="/parse_segmentation"
            )
            return result

    PALIGEMMA_API = PaligemmaApi()