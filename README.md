# ChatLite

This is my first AI project. The goal of this project is to be able to use a Large Language Model (LLM) to create a TL;DR from user-provided data (ex. procedures on completing tasks). The sub-goal is to gain a good working knowledge of manipulating LLMs.

All software and models will be run locally with open-source to maintain accessibility, control, and customization.

![Llama RAG](./Images/llama_tldr.jpg)

## Steps
1. Learn how to be able to interact with a transformer model. I will be using the Llama 3.2 3B Instruct checkpoint and wrapping it using Hugging Face Transformers in order to submit user-generated queries and receive responses from the model.
2. Learn how to tokenize and making embeddings of user-provided data in a usable form so that the LLM can efficiently parse the data. 
3. Create a user-friendly interface that will take queries about procedures and return steps for completion of the requested task.

## Learning Outcomes
1. Develop Advanced Python Skills: Strengthen your Python proficiency for machine learning, mastering efficient code writing and debugging in practical ML applications.
2. Master PyTorch Fundamentals: Build and train neural networks using PyTorch, gaining hands-on experience with tensors, model architectures, and the autograd system.
3. Achieve In-depth Knowledge of Transformers: Understand and apply transformer architectures for NLP tasks, focusing on attention mechanisms and model fine-tuning with Hugging Face Transformers.
4. Comprehend Hardware Requirements for LLMs: Analyze the impact of hardware, memory, and model parameter sizes on LLM performance, exploring multi-GPU and cloud-based solutions for scalability.

## Installation
1. CUDA v12.6 (to use the power of local GPUs)
2. PyTorch
3. Transformers (architecture)
4. Hugging Face quantized Meta Llama 3.2B Instruct (checkpoint)
5. Langchain (Retrieval Augmented Generation)

```bash
git clone https://github.com/kunit17/ChatLite.git
cd ChatLite