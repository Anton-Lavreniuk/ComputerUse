# Computer use agent

This is a simple program that uses Vision Language Models (VLMs) and tool calling to perform user-specified tasks.
Currently, it can use the Google and OpenAI models as the primary VLMs, and a Huggingface model (Paligemma) as a secondary VLM for object detection.
The program can perform rudimentary tasks such as opening applications, typing text, moving the cursor, and clicking on the screen.

# Setup

1. Clone the repository
```bash
git clone https://github.com/username/ComputerUse.git
cd ComputerUse
```
2. Activate the virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up environment variables
Copy the `.env.example` file and rename it to `.env`. Fill in the required values with corresponding keys.
Note: THe .env.example file contains some of my own keys, sufficient for using the app for short periods of time with weak models.
5. Run the program
```bash
python main.py
```

## Known issues
- The GUI freezes during task execution. \
- Not tested with only 1 screen. On several screens works only with screen 1. \
- Generally poor performance on complex tasks (early version)

## If you get an error saying the handshake operation timed out, try again. This error is thrown by the free Huggingface API.





# Usage example:

Query: 

```
"Open Paint, then draw something using the default brush"
```

Result:

```
Response: <thinking>
My task is to open Paint and draw something using the default brush. Currently, the screen shows a web browser. I need to open the Start menu to search for Paint.

First, I will press the Windows key to open the Start menu.
</thinking>

<tools>
[
    {"Press_key_tool":{"key":"win"}}
]
</tools>
Response: <thinking>
The Start menu is open. I need to search for Paint. I will type "Paint" and press Enter to open it.
</thinking>

<tools>
[
    {"Type_text_tool":{"text":"Paint"}},
    {"Press_key_tool":{"key":"enter"}}
]
</tools>
Response: <thinking>
Paint is open, and I can see the canvas. I need to draw something using the default brush. The cursor is currently positioned at (1274, 535). I will move the cursor to the canvas and draw a simple shape.
</thinking>

<tools>
[
    {"Move_cursor_tool":{"x":500,"y":300}}
]
</tools>
Response: <thinking>
The cursor is now positioned on the canvas. I will draw a simple shape by dragging the cursor.
</thinking>

<tools>
[
    {"Drag_relative_tool":{"x_offset":100,"y_offset":0}},
    {"Drag_relative_tool":{"x_offset":0,"y_offset":100}},
    {"Drag_relative_tool":{"x_offset":-100,"y_offset":0}},
    {"Drag_relative_tool":{"x_offset":0,"y_offset":-100}}
]
</tools>
Response: <thinking>
I have successfully drawn a simple square on the canvas using the default brush in Paint. The task is complete.
</thinking>

<tools>
[
    {"Terminate_tool":{}}
]
</tools>
```
