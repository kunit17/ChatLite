# Use Ubuntu as the base image
FROM ubuntu:latest as llama

# Set environment variable to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies: git, curl, bash, and Git LFS
RUN apt-get update && \
    apt-get install -y \
    git \
    curl \
    bash \
    ca-certificates && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get install -y git-lfs && \
    rm -rf /var/lib/apt/lists/*

# Define build-time arguments for Hugging Face username and token
ARG HF_USERNAME
ARG HF_TOKEN

# Set up the working directory
WORKDIR /app

# Copy the contents of the local directory to the /app directory in the container
COPY . /app

# Check if the folder exists and conditionally run the git commands
RUN if [ ! -d "/app/Llama-3.2-3B-Instruct" ]; then \
        git lfs install && \
        git clone https://${HF_USERNAME}:${HF_TOKEN}@huggingface.co/meta-llama/Llama-3.2-3B-Instruct /app; \
    fi

# Use an image with Jupyter notebook and PyTorch pre-installed as the base image
FROM quay.io/jupyter/pytorch-notebook:cuda12-python-3.11.8

# Set the working directory to the default Jupyter directory
WORKDIR /home/jovyan

# Copy the contents of the local directory to the container's /home/jovyan
COPY . /home/jovyan
COPY --from=llama /app /home/jovyan

# Install necessary Python libraries
RUN pip install --no-cache-dir transformers

RUN pip install git+https://github.com/huggingface/accelerate

# Expose the port for Jupyter notebook
EXPOSE 8888

# Command to run when the container starts
CMD ["start-notebook.sh", "--NotebookApp.port=8888", "--NotebookApp.ip='*'", "--NotebookApp.open_browser=False"]
