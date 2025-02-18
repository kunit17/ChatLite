from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from pathlib import Path
import markdown

class ChatGenerator:
    def __init__(self):
        checkpoint = (Path.cwd()) / 'Llama-3.2-3B-Instruct' # Set the model checkpoint path
        self.text_generator = pipeline(
            "text-generation",
            model=AutoModelForCausalLM.from_pretrained(
                checkpoint,
                torch_dtype=torch.float16,
                local_files_only=True,
                device_map="auto"  # Automatically uses GPU if available
                ),
            tokenizer=AutoTokenizer.from_pretrained(checkpoint), # Load tokenizer
            torch_dtype=torch.float16,
            device_map="auto"  # Auto-detect and use GPU
        )
        self.history = ""

    def chat_history(self, get_q, response):
        # Append the question and response to the chat history
        self.history += get_q + response

    def generate_response(self, get_q: str, top_documents: list):
        # Generate sequences
        prompt = f"I will ask the following question: {self.history}\n{get_q}. Answer that question incorporating the following information as the core of the response: \n\n{'\n\n'.join(top_documents)}. \n\n Answer in 3 sentences or less."
        response = self.text_generator(
            prompt,
            do_sample=True,
            top_k=2,
            temperature=0.2,
            num_return_sequences=1,
            eos_token_id=self.text_generator.tokenizer.eos_token_id,
            truncation=True,
            max_length=100000
        )[0]['generated_text']  
        
        response_without_chathistory = response.replace(prompt, "").strip()
        # Convert generated response to HTML using markdown
        html_output = markdown.markdown(response_without_chathistory)  # Converts the response to HTML 
        self.chat_history(get_q, response_without_chathistory)       
        return html_output  # Return HTML output