import pyautogui
from llama_index.core import SimpleDirectoryReader
from llama_index.core.tools import FunctionTool

from models import Model


class MagicClickTool:
    def __init__(self):
        self.model = Model.PALIGEMMA_API

    def _move(self, query: str):
        """Detect the object in the text query and click on it"""
        result = self.model.process(query="Detect " + query, image_route="screenshot.png")
        print(result)
        from PIL import Image
        if not result["annotations"]:
            return "No object matching the text query detected."
        img = Image.open(result["annotations"][0]["image"])
        pixels = img.load()
        width, height = img.size
        min_x, max_x, min_y, max_y = width, 0, height, 0

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a > 0:
                    if x < min_x: min_x = x
                    if x > max_x: max_x = x
                    if y < min_y: min_y = y
                    if y > max_y: max_y = y

        cx = (min_x + max_x) // 2
        cy = (min_y + max_y) // 2
        pyautogui.click(cx, cy)

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._move,
            name="Magic_click_tool",
            description="Detect the object in the text query and click on it. Examples of the input format you MUST always follow: 'small Submit button', 'Email text field'"
        )
class MoveCursorTool:
    def __init__(self):
        pass

    def _move_relative(self, x: int, y: int):
        """Move the cursor to some position"""
        pyautogui.moveTo(x, y)

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._move_relative,
            name="Move_cursor_tool",
            description="Move the cursor to some x and y position. Use small movements (10-20 pixels) for precision."
        )
class MoveRelativeTool:
    def __init__(self):
        pass

    def _move_relative(self, x_offset: int, y_offset: int):
        """Move the cursor relative to current position"""
        pyautogui.moveRel(x_offset, y_offset)

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._move_relative,
            name="Move_relative_tool",
            description="Move the cursor relative to its current position using x and y offsets. Use small movements (10-20 pixels) for precision."
        )

class ClickTool:
    def __init__(self):
        pass

    def _click(self):
        """Click at current cursor position"""
        pyautogui.click()

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._click,
            name="Click_tool",
            description="Clicks the current cursor position. Make sure to move the cursor to the desired position first, take a new screenshot, and only then click."
        )

class DoubleClickTool:
    def __init__(self):
        pass

    def _double_click(self):
        """Double click at current cursor position"""
        pyautogui.doubleClick()

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._double_click,
            name="Double_click_tool",
            description="Performs a double click at the current cursor position."
        )

class RightClickTool:
    def __init__(self):
        pass

    def _right_click(self):
        """Right click at current cursor position"""
        pyautogui.rightClick()

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._right_click,
            name="Right_click_tool",
            description="Performs a right click at the current cursor position."
        )

class DragToTool:
    def __init__(self):
        pass

    def _drag_to(self, x: int, y: int):
        """Drag cursor to absolute coordinates"""
        pyautogui.dragTo(x, y)

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._drag_to,
            name="Drag_to_tool",
            description="Drags from current position to specified coordinates while holding mouse button."
        )

class DragRelativeTool:
    def __init__(self):
        pass

    def _drag_relative(self, x_offset: int, y_offset: int):
        """Drag cursor relative to current position"""
        pyautogui.dragRel(x_offset, y_offset)

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
        """Scroll the mouse wheel"""
        pyautogui.scroll(amount)

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
        """Type text with specified interval between keypresses"""
        pyautogui.write(text, interval=interval)

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
        """Press a key specified number of times"""
        pyautogui.press(key, presses=presses, interval=interval)

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._press_key,
            name="Press_key_tool",
            description="Presses a key specified number of times with configurable interval. You must use this tool for singular key presses such as win or caps lock. Keys include letters, numbers, and special keys like 'enter', 'tab', 'space', 'win', arrow keys, etc."
        )

class HotkeyTool:
    def __init__(self):
        pass

    def _hotkey(self, *keys):
        """Press multiple keys simultaneously"""
        pyautogui.hotkey(*keys)
        return "Keys pressed: " + ", ".join(keys)

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._hotkey,
            name="Multikey_tool",
            description="Presses one or multiple keys simultaneously for keyboard shortcuts. Example keys: 'ctrl', 'alt', 'shift', 'command', letters, numbers."
        )


class SleepTool:
    def __init__(self):
        pass

    def _sleep(self, seconds: float):
        """Wait for specified duration"""
        pyautogui.sleep(seconds)

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._sleep,
            name="Sleep_tool",
            description="Waits for specified number of seconds. Use this to wait for applications to load or animations to complete."
        )

class TerminateTool:
    def __init__(self):
        pass

    def _terminate(self):
        """Terminate the program"""
        return "terminate_string"

    def create_tool(self):
        return FunctionTool.from_defaults(
            fn=self._terminate,
            name="Terminate_tool",
            description="Terminates the current task and ends the thinking loop. Use this when you have successfully completed the task."
        )