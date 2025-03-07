from gui import GUI
from models import Model

if __name__ == "__main__":
    model = Model.GPT_4_O
    app = GUI(model)
    app.run()
