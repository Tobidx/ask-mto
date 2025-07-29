import os
import pytesseract
from pdf2image import convert_from_path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def load_pdf_with_ocr(pdf_path: str) -> str:
    """
    Convert each page of the PDF into an image and extract text via OCR.
    Returns the full concatenated text.
    """
    # Ensure Tesseract and Poppler are installed on your system
    images = convert_from_path(pdf_path, dpi=300)
    text_pages = []
    for page in images:
        page_text = pytesseract.image_to_string(page)
        text_pages.append(page_text)
    return "\n\n".join(text_pages)

def load_pdf_chunks(pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Load the PDF via OCR, then split into overlapping text chunks.
    Returns a list of langchain Document objects.
    """
    full_text = load_pdf_with_ocr(pdf_path)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    texts = splitter.split_text(full_text)
    documents = [Document(page_content=txt) for txt in texts]
    print(f"✅ OCR extracted and split into {len(documents)} chunks.")
    return documents

def create_vectorstore(chunks, index_path: str = "vectorstore"):
    """
    Create (or overwrite) a FAISS vectorstore from the given chunks.
    Saves locally under `index_path`.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not set in environment variables")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_path)
    print(f"✅ Vectorstore built and saved to '{index_path}'.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build FAISS vectorstore from a PDF via OCR")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--index_path", default="vectorstore", help="Directory to save the vectorstore")
    args = parser.parse_args()

    docs = load_pdf_chunks(args.pdf_path)
    create_vectorstore(docs, args.index_path)
