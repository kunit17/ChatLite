import tkinter as tk

class QuestionGUI:
    def __init__(self, master, model):
        self.master = master
        self.model = model  # Store model for later use
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Ask a question:")
        self.label.pack()

        self.entry = tk.Entry(self.master, width=50)
        self.entry.pack()
        self.entry.bind("<Return>", self.submit)  # Bind Enter key to submit function

        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        self.submit_button.pack()

        self.response_label = tk.Label(self.master, text="", witdh=300, wraplength=500)
        self.response_label.pack()

    def submit(self, event=None):
        question = self.entry.get()
        response = self.model.generate_response(question)  # Generate response using model
        self.response_label.config(text=response)
        self.entry.delete(0, tk.END)  # Clear entry field
        self.submit_button.invoke()  # Simulate click submit button when you press Enter

test = QuestionGui()

submit.test