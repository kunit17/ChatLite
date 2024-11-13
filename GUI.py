import tkinter as tk
from tkhtmlview import HTMLLabel
from tkinter import messagebox
import asyncio
from RAG import get_top_documents_sync  # Assuming you've created this function as per the previous steps

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

        # Loading indicator (optional)
        self.loading_label = tk.Label(self.master, text="", width=20)
        self.loading_label.pack()

    def submit(self, event=None):
        question = self.entry.get()

        # Clear the previous response and show a loading message
        self.response_label.set_html("")
        self.loading_label.config(text="Loading...")

        try:
            # Get top 4 similar documents asynchronously and sync it for GUI use
            top_documents = get_top_documents_sync(question)

            if not top_documents:
                raise ValueError("No similar documents found.")

            # Pass the top documents to the model and get the response
            response = self.model.generate_response(question, top_documents)

            # Display the generated response
            self.response_label.set_html(response)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.response_label.set_html("Sorry, an error occurred while processing your request.")

        finally:
            # Clear loading indicator and entry field
            self.loading_label.config(text="")
            self.entry.delete(0, tk.END)  # Clear entry field
