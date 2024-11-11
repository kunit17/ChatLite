from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from pathlib import Path


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

    def generate_response(self, get_q: str):

        # Generate sequences
        return self.text_generator(
            get_q,
            do_sample=True,
            top_k=4,
            temperature=0.5,
            num_return_sequences=1,
            eos_token_id=self.text_generator.tokenizer.eos_token_id,
            truncation=True,
            max_length=1000
        )

