import tkinter as tk
from tkhtmlview import HTMLLabel

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

        self.response_label = HTMLLabel(self.master, html="", width=100, height=20)
        self.response_label.pack(fill=tk.BOTH, expand=True)

    def submit(self, event=None):
        question = self.entry.get()
        response = self.model.generate_response(question)  # Generate response using model
        self.response_label.set_html(response)  # Use set_html to display the HTML response
        self.entry.delete(0, tk.END)  # Clear entry field