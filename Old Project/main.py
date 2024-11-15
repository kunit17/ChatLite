import tkinter as tk
from GUI import QuestionGUI
from Model import ChatGenerator

def main():
    root = tk.Tk()
    model = ChatGenerator()  # Initialize model here
    app = QuestionGUI(root, model)  # Pass model to QuestionGUI
    root.mainloop()

if __name__ == "__main__":
    main()