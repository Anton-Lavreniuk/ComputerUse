
import os
import re

from dotenv import load_dotenv
from llama_index.multi_modal_llms.huggingface import HuggingFaceMultiModal

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
from llama_index.llms.openrouter import OpenRouter
from gradio_client import Client, handle_file
import os
from io import BytesIO
from PIL import Image
import base64
from openai import OpenAI
from llama_index.multi_modal_llms.gemini import GeminiMultiModal


class OpenRouterApi:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def process(self, query, img_bytes, use_light_model=True):
        b64 = base64.b64encode(img_bytes).decode("utf-8")
        data_uri = f"data:image/png;base64,{b64}"
        user_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": f"You are a visual grounding model. Provided with a query and a screenshot, first reason about it's position, then find the matching object on the screenshot and return it's x and y coordinates like (x,y). Response example: The button is located on the bottom left corner of the screen - (200, 700). Here is the query: {query}"
},
                {"type": "image_url", "image_url": {"url": data_uri}}
            ]
        }

        completion = self.client.chat.completions.create(
            model= "google/gemini-2.5-flash-preview" if use_light_model else "google/gemini-2.5-pro-preview",
            messages=[user_message],
            extra_headers={
            }
        )

        return completion.choices[0].message.content
    def expose_completion(self, prompt, image_documents):
        data_uri = f"data:image/png;base64,{image_documents}"
        user_message = {
            "role": "user",
            "content": [
                {"type": "text",
                 "text": prompt
                 },
                {"type": "image_url", "image_url": {"url": data_uri}}
            ]
        }

        response = self.client.chat.completions.create(
            model="google/gemini-2.5-flash-preview",
            messages=[ user_message ],
            extra_headers={
            }
        ).text

        return response

GEMINI_GROUNDING = OpenRouterApi()
if __name__ == "__main__":
    with open("step_1.png", "rb") as f:
        image_bytes = f.read()

    query = "Find the More tools button"
    result = OpenRouterApi().process(query, image_bytes, False)
    print("Model response:", result)
    match = re.search(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)", result)
    print(match)
    match = match.group(0) if match else ""
    print(match)
    x, y = map(int, match.strip("()").split(","))
    img = Image.open(BytesIO(image_bytes))
    width, height = img.size
    x_abs = round(x * width / 1000)
    y_abs = round(y * height / 1000)

    print("Model response:", x_abs, y_abs)

class Model:

    # GEMINI_1_5_PRO = GeminiMultiModal(
    #         model_name="models/gemini-1.5-pro",
    #         api_key=os.environ.get("GEMINI_API_KEY"),
    #         temperature=0
    #     )

    GPT_4_O = OpenAIMultiModal(model="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY"), image_detail="high", temperature=0)
    # GEMINI_2_5_FLASH = OpenRouter(
    # api_key=os.getenv("OPENROUTER_API_KEY"),
    # model="google/gemini-2.5-flash-preview")

    GEMINI_GROUNDING = OpenRouterApi()
