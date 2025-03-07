import json
import os
import re

from PIL import ImageGrab, ImageDraw
from llama_index.core import SimpleDirectoryReader
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.schema import ImageNode
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
import pyautogui
from dotenv import load_dotenv

from prompt_storage import PromptStorage
import llm_tools


class Processor:

    def __init__(self, model):
        load_dotenv()
        self.model = model
        self.tools = [
            llm_tools.ClickTool().create_tool(),
                      llm_tools.MoveCursorTool().create_tool(),
                      llm_tools.MoveRelativeTool().create_tool(),
                      llm_tools.DoubleClickTool().create_tool(),
                      llm_tools.RightClickTool().create_tool(),
                      llm_tools.MagicClickTool().create_tool(),
                      # llm_tools.DragToTool().create_tool(),
                      llm_tools.DragRelativeTool().create_tool(),
                      llm_tools.ScrollTool().create_tool(),
                      llm_tools.TypeTextTool().create_tool(),
                      llm_tools.PressKeyTool().create_tool(),
                      llm_tools.HotkeyTool().create_tool(),
                      # llm_tools.MouseDownTool().create_tool(),
                      # llm_tools.MouseUpTool().create_tool(),
                      llm_tools.SleepTool().create_tool(),
                      llm_tools.TerminateTool().create_tool()
                      ]
        self.tool_info = [{"Name": tool.metadata.name, "Description": tool.metadata.description,
                           "Schema": tool.metadata.fn_schema_str} for tool in self.tools]
        self.MAX_STEPS = 10
        self.move_count = 0

    def take_screenshot(self):
        # Take the screenshot
        # Grab smaller part of the screen each time move is called
        img = ImageGrab.grab(include_layered_windows=True)
        # Get the cursor position
        x, y = pyautogui.position()
        width, height = img.size
        # if self.move_count != 0:
        # if False:
        #     k = 50  # Pixels to crop for each move action, centered around the cursor
        #     reduction = self.move_count * k
        #
        #     new_width = max(width - reduction, 600)
        #     new_height = max(height - reduction, 300)
        #     left = max(x - new_width // 2, 0)
        #     top = max(y - new_height // 2, 0)
        #     right = min(left + new_width, width)
        #     bottom = min(top + new_height, height)
        #     bounds = (left, top, right, bottom)
        #     img = ImageGrab.grab(bounds)

        # Create an ImageDraw object
        # draw = ImageDraw.Draw(img)
        # Draw 4 reference circles
        # Description for the llm
        # desc = "4 blue circles"
        # cursor_desc = "One red circle"
        # p1 = width / 4, height / 4
        # p2 = 3 * width / 4, height / 4
        # p3 = width / 4, 3 * height / 4
        # p4 = 3 * width / 4, 3 * height / 4
        # radius = 20
        # color = (0, 0, 255, 128)
        # draw.ellipse((p1[0] - radius, p1[1] - radius, p1[0] + radius, p1[1] + radius), fill=color)
        # draw.ellipse((p2[0] - radius, p2[1] - radius, p2[0] + radius, p2[1] + radius), fill=color)
        # draw.ellipse((p3[0] - radius, p3[1] - radius, p3[0] + radius, p3[1] + radius), fill=color)
        # draw.ellipse((p4[0] - radius, p4[1] - radius, p4[0] + radius, p4[1] + radius), fill=color)

        # Draw a circle at the cursor position
        # draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(255, 0, 0, 128))

        img.save('screenshot.png')
        # Save the screenshot
        # screenshot = pyautogui.screenshot()
        # screenshot.save("screenshot.png")
        # return f"Image size: W:{width}, H:{height}. Reference points: {desc}, at coordinates {p1}, {p2}, {p3}, {p4} respectively. Cursor :{cursor_desc} position: {x}, {y}"
        return f"Image size: W:{width}, H:{height}. Cursor position: {x}, {y}"

    def process_task(self, task: str):
        image_metadata = self.take_screenshot()
        task_memory = [PromptStorage.SYSTEM_PROMPT.format(tools=self.tool_info, task=task,
                                                          image_metadata=image_metadata)]
        def get_prompt(image_metadata):
            return "\n".join(task_memory) + "\n" + image_metadata

        for i in range(0, self.MAX_STEPS):
            print("---Executing step", i, "---")

            image_metadata = self.take_screenshot()

            image_documents = SimpleDirectoryReader(
                input_files=["screenshot.png"]
            ).load_data()

            response = self.model.complete(
                prompt=get_prompt(image_metadata),
                image_documents=image_documents
            ).text
            print(response)
            task_memory.append(response)

            should_terminate = False
            try:
                pattern = r'<tools>(.*?)</tools>'
                match = re.search(pattern, response, re.DOTALL)
                content = match.group(1).strip()
                json_tool_calls = json.loads(content)
                for tool_call in json_tool_calls:
                    for key, value in tool_call.items():
                        for tool in self.tools:
                            if tool.metadata.name == key:
                                print(f"Calling tool {key} with args {value}")
                                res = tool.fn(**value)
                                if res == "terminate_string":
                                    # Terminate the task
                                    should_terminate = True
                                    break
                                if res:
                                    task_memory.append("\nTool call returned a response: " + res + "\n")
                        if should_terminate:
                            break
                    if should_terminate:
                        break
            except:
                pass

            yield response

            if should_terminate:
                break

        print("Task execution stopped")
