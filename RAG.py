import asyncio
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer

# Directory containing PDFs
pdf_dir = Path.cwd() / 'Data'

# Ensure the directory exists
if not pdf_dir.exists():
    raise ValueError(f"Directory {pdf_dir} does not exist")

# Function to load PDFs asynchronously
async def process_pdfs():
    chunked_docs = []
    for pdf_path in pdf_dir.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        async for page in loader.alazy_load():  # async loading
            chunked_docs.append(page)
    return chunked_docs

# Async function to run everything
async def main():
    # Load PDF documents asynchronously
    chunked_docs = await process_pdfs()

    # Load the SentenceTransformer model
    model_dir = r"C:\Users\barbu\Projects\lrn\stella_en_400M_v5"
    model = SentenceTransformer(
        model_dir,
        trust_remote_code=True,
        device="cuda",
        config_kwargs={"use_memory_efficient_attention": True, "unpad_inputs": True}
    )

    # Encode the chunked documents
    doc_texts = [doc.page_content for doc in chunked_docs]
    doc_embeddings = model.encode(doc_texts, convert_to_tensor=True)

    # Prompt user for a query
    user_query = input("Enter a query to find similar documents: ")

    # Encode the input query
    query_embedding = model.encode([user_query], convert_to_tensor=True)

    # Calculate similarity between the query and each document
    similarities = model.similarity(query_embedding, doc_embeddings)

    # Print the similarity results
    print("\nSimilarity scores between your query and documents:")
    print(similarities)

    # Check if we have valid similarity results
    if similarities.shape[1] > 0:  # Ensure there are scores in similarities
        # Get the top 4 most similar documents
        num_results = min(4, similarities.shape[1])  # Limit results to 4 or fewer if there aren't enough
        top_indices = similarities[0].argsort(descending=True)[:num_results]  # Sort in descending order

        # Print the top similar documents
        print("\nTop most similar documents to your query:")
        for i, idx in enumerate(top_indices):
            print(f"\nRank {i + 1}:")
            print(f"Similarity: {similarities[0][idx]:.4f}")
            print(f"Document: {doc_texts[idx][:500]}...")  # Display the first 500 characters of the document
    else:
        print("No results found.")

# Run the async function
asyncio.run(main())
