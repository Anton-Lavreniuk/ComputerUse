from gui import GUI
from models import Model

if __name__ == "__main__":
    model = Model.GEMINI_2_0_FLASH
    app = GUI(model)
    app.run()
