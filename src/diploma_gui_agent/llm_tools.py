import json
import re
from io import BytesIO
import pyautogui
from llama_index.core.tools import FunctionTool
from .models import Model
from PIL import Image


class MagicClickTool:
    def __init__(self):
        self.model = Model.GEMINI_GROUNDING

    def _move(self, **kwargs):
        query = kwargs.get("query", None)
        try:
            clicks = int(query["N"])
        except:
            clicks = 1

        print("Magic click query : ", query)
        screenshot = kwargs.get("screenshot", None)
        print(type(screenshot), isinstance(screenshot, bytes))
        if isinstance(screenshot, (bytes, bytearray)):
            print(len(screenshot))
        result = self.model.process(query=query, img_bytes=screenshot, use_light_model=False)
        print("Magic click result : ", result)

        match = re.search(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)", result)
        match = match.group(0) if match else ""
        try:
            x, y = map(int, match.strip("()").split(","))
            img = Image.open(BytesIO(screenshot))
            width, height = img.size
            x_abs = round(x * width / 1000)
            y_abs = round(y * height / 1000)

            x, y = x_abs, y_abs

            return f"pyautogui.click({x},{y}, clicks={clicks})\n"
        except Exception as e:
            return "pass"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._move,
            name="Magic_click_tool",
            description="Detect the object in the text query and click on it N times. N is 1 by default. Example of the input format you MUST always follow: {\"query\":\"Find the Settings button on the left sidebar, in the drop down menu\", \"N\": 1}"
        )
class MagicRightClickTool:
    def __init__(self):
        self.model = Model.GEMINI_GROUNDING

    def _move(self, **kwargs):
        query = kwargs.get("query", "")
        print("Magic right click query : ", query)
        screenshot = kwargs.get("screenshot", None)
        print(type(screenshot), isinstance(screenshot, bytes))
        if isinstance(screenshot, (bytes, bytearray)):
            print(len(screenshot))
        result = self.model.process(query=query, img_bytes=screenshot, use_light_model=False)
        print("Magic click result : ", result)

        match = re.search(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)", result)
        match = match.group(0) if match else ""
        x, y = map(int, match.strip("()").split(","))
        img = Image.open(BytesIO(screenshot))
        width, height = img.size
        x_abs = round(x * width / 1000)
        y_abs = round(y * height / 1000)

        x, y = x_abs, y_abs

        return f"pyautogui.click({x},{y}, button='right')\n"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._move,
            name="Magic_right_click_tool",
            description="Detect the object in the text query and right click on it once. Example of the input format you MUST always follow: {\"query\":\"Find the Settings button on the left sidebar, in the drop down menu\"}"
        )


class DragRelativeTool:
    def __init__(self):
        pass

    def _drag_relative(self, x_offset: int, y_offset: int):
        return f"pyautogui.dragRel({x_offset},{y_offset})\n"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._drag_relative,
            name="Drag_relative_tool",
            description="Drags relative to current position using x and y offsets while holding mouse button."
        )

class ScrollTool:
    def __init__(self):
        pass

    def _scroll(self, amount: int):
        return f"pyautogui.scroll({amount})\n"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._scroll,
            name="Scroll_tool",
            description="Scrolls the mouse wheel. Positive numbers scroll up, negative numbers scroll down."
        )

class TypeTextTool:
    def __init__(self):
        pass

    def _type_text(self, text: str, interval: float = 0.1):
        return f"pyautogui.write({text!r}, interval={interval})\n"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._type_text,
            name="Type_text_tool",
            description="Types the specified text with a configurable interval between keypresses. Default interval is 0.1 seconds."
        )

class PressKeyTool:
    def __init__(self):
        pass

    def _press_key(self, key: str, presses: int = 1, interval: float = 0.2):
        return f"pyautogui.press({key!r}, presses={presses}, interval={interval})\n"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._press_key,
            name="Press_key_tool",
            description="Presses a key specified number of times with configurable interval. You must use this tool for singular key presses such as win or caps lock. Keys include letters, numbers, and special keys like 'enter', 'tab', 'space', 'win', arrow keys, etc."
        )

class HotkeyTool:
    def __init__(self):
        pass

    def _hotkey(self, keys):
        args = ", ".join(repr(k) for k in keys)
        return f"pyautogui.hotkey({args})\n"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._hotkey,
            name="Multikey_tool",
            description="Presses one or multiple keys simultaneously for keyboard shortcuts. Example keys: 'ctrl', 'alt', 'shift', 'command', letters, numbers. Input format: {\"keys\":[\"alt\", \"e\"]}"
        )

class SleepTool:
    def __init__(self):
        pass

    def _sleep(self):
        return f"pyautogui.sleep(2)\n"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._sleep,
            name="Sleep_tool",
            description="Waits for 2 seconds. Use this to wait for applications to load or animations to complete."
        )

class TerminateTool:
    def __init__(self):
        pass

    def _terminate(self):
        return "terminate_string\n"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._terminate,
            name="Terminate_tool",
            description="Terminates the current task and ends the thinking loop. Use this when you have successfully completed the task."
        )
