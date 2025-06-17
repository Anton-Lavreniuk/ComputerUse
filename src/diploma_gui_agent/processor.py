import json
import re
from collections.abc import Sequence
from llama_index.core.schema import ImageDocument
from PIL import ImageGrab
from llama_index.core import SimpleDirectoryReader
import pyautogui
from dotenv import load_dotenv

from . import llm_tools
from .models import Model, OpenRouterApi
from .prompt_storage import PromptStorage


class Processor:

    def __init__(self, model = None):
        load_dotenv()
        self.model = model or None
        self.tools = [
                      llm_tools.MagicRightClickTool().create_tool(),
                      llm_tools.MagicClickTool().create_tool(),
                      # llm_tools.DragRelativeTool().create_tool(),
                      llm_tools.ScrollTool().create_tool(),
                      llm_tools.TypeTextTool().create_tool(),
                      llm_tools.PressKeyTool().create_tool(),
                      llm_tools.HotkeyTool().create_tool(),
                      llm_tools.SleepTool().create_tool(),
                      llm_tools.TerminateTool().create_tool()
                      ]
        self.tool_info = [{"Name": tool.metadata.name, "Description": tool.metadata.description,
                           "Schema": tool.metadata.fn_schema_str} for tool in self.tools]
        self.MAX_STEPS = 10
        self.history = []
        self.move_count = 0

    def process_task(self, task: str, screenshot, metadata):
        task_memory = [PromptStorage.SYSTEM_PROMPT.format(tools=self.tool_info, task=task,
                                                          image_metadata=metadata)]

        def get_prompt(image_metadata):
            print(len(self.history))
            return "\n".join(task_memory) + "\n" + "History:" + "\n".join(self.history[-2:]) + "\n"


        print("---Executing step---")

        image_metadata = metadata
        # image_documents = [ImageDocument(image=screenshot)]

        response = OpenRouterApi().process(
            query=get_prompt(image_metadata),
            img_bytes=screenshot
        )
        print(response)
        task_memory.append(response)
        try:
            pattern = r'<thinking>(.*?)</thinking>'
            match = re.search(pattern, response, re.DOTALL)
            self.history.append(match.group(1).strip())
        except:
            self.history.append(response)


        pattern = r'<tools>(.*?)</tools>'
        match = re.search(pattern, response, re.DOTALL)
        try:
            content = match.group(1).strip()
        except:
            self.history.append("Wrong response format! Use <tools></tools> tags!")
            return "WAIT"
        json_tool_calls = json.loads(content)
        for tool_call in json_tool_calls:
            for name, args in tool_call.items():
                for tool in self.tools:
                    if tool.metadata.name == name:
                        print("Calling tool with args:" + str(args))
                        if "Magic" in name:
                            print("Magic tool detected, adding screenshot to args")
                            args["screenshot"] = screenshot
                        cmd = tool.fn(**args)
                        if name == "Sleep_tool":
                            return "WAIT"
                        elif name == "Terminate_tool":
                            return "DONE"
                        else:
                            print(f"Yielding: ```python\n{cmd}```")
                            return f"```python\n{cmd}```"



    print("Task execution stopped")
