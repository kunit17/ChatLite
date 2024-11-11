# Use Ubuntu as the base image
FROM ubuntu:latest as llama

# Set environment variable to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies: git, curl, bash, and Git LFS
RUN apt-get update && \
    apt-get install -y \
    git \                          # Install Git for version control
    curl \                         # Install curl for downloading resources
    bash \                         # Install bash to ensure bash scripts can run
    ca-certificates && \           # Install CA certificates to allow SSL communication
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \  # Install Git LFS (Large File Storage) repository
    apt-get install -y git-lfs && \  # Install Git LFS package
    rm -rf /var/lib/apt/lists/*    # Clean up APT cache to reduce image size

# Define build-time arguments for Hugging Face username and token
ARG HF_USERNAME                   # This argument will store the Hugging Face username
ARG HF_TOKEN                      # This argument will store the Hugging Face token for authentication

# Set up the working directory
WORKDIR /app                        # Set the working directory to `/app` for subsequent instructions

# Copy the contents of the local directory to the /app directory in the container
COPY . /app                        # Copy all files from the local directory into `/app` inside the container

# Check if the folder exists and conditionally run the git commands
RUN if [ ! -d "/app/Llama-3.2-3B-Instruct" ]; then \  # If the folder `/app/Llama-3.2-3B-Instruct` does not exist,
        git lfs install && \         # Install Git LFS if not already installed
        git clone https://${HF_USERNAME}:${HF_TOKEN}@huggingface.co/meta-llama/Llama-3.2-3B-Instruct /app; \  # Clone the Llama repository
    fi

# Use an image with Jupyter notebook and PyTorch pre-installed as the base image
FROM quay.io/jupyter/pytorch-notebook:cuda12-python-3.11.8  # Use the Jupyter notebook image with PyTorch and CUDA support

# Set the working directory to the default Jupyter directory
WORKDIR /home/jovyan                # Change the working directory to `/home/jovyan`, the default directory for Jupyter notebooks

# Copy the contents of the local directory to the container's /home/jovyan
COPY . /home/jovyan                  # Copy all files from the local directory to `/home/jovyan` in the container
COPY --from=llama /app /home/jovyan   # Copy the `/app` directory from the previous stage (`llama`) to `/home/jovyan` in this stage

# Install necessary Python libraries
RUN pip install --no-cache-dir transformers  # Install the Hugging Face `transformers` library without caching to reduce image size

RUN pip install git+https://github.com/huggingface/accelerate  # Install the `accelerate` library from the Hugging Face GitHub repository

# Expose the port for Jupyter notebook
EXPOSE 8888  # Expose port 8888 to access Jupyter notebook in the container

# Command to run when the container starts
CMD ["start-notebook.sh", "--NotebookApp.port=8888", "--NotebookApp.ip='*'", "--NotebookApp.open_browser=False"]  # Start Jupyter notebook without opening the browser, binding it to all network interfaces on port 8888
