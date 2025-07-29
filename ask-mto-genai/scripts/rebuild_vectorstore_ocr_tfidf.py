#!/usr/bin/env python3

import os
import sys
import re
from dotenv import load_dotenv
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

load_dotenv()

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def preprocess_image(image):
    """Enhance image quality for better OCR"""
    # Convert to grayscale
    if image.mode != 'L':
        image = image.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.5)
    
    # Apply slight blur to reduce noise
    image = image.filter(ImageFilter.MedianFilter(size=3))
    
    return image

def extract_text_with_ocr(pdf_path: str, max_pages: int = 50) -> str:
    """
    Extract text from PDF using OCR with image preprocessing
    """
    try:
        print(f"Converting PDF to images for enhanced OCR (max {max_pages} pages)...")
        images = convert_from_path(
            pdf_path, 
            dpi=300, 
            first_page=1, 
            last_page=max_pages,
            thread_count=4
        )
        
        text_content = []
        
        for i, image in enumerate(images):
            print(f"Processing page {i+1}/{len(images)} with enhanced OCR...")
            
            # Preprocess image for better OCR
            processed_image = preprocess_image(image)
            
            # OCR with optimized configuration
            custom_config = r'--oem 3 --psm 6'
            
            try:
                text = pytesseract.image_to_string(processed_image, config=custom_config)
                
                # Clean the extracted text
                text = re.sub(r'[^\w\s.,!?()\[\]{}:;]', ' ', text)  # Remove special chars
                text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
                text = text.strip()
                
                if text and len(text) > 100:  # Minimum text length
                    text_content.append(text)
                    print(f"  ✓ Extracted {len(text)} characters from page {i+1}")
                else:
                    print(f"  - Page {i+1} has minimal readable text")
                    
            except Exception as e:
                print(f"  ✗ OCR failed for page {i+1}: {e}")
                continue
        
        full_text = "\n\n".join(text_content)
        print(f"Enhanced OCR extracted {len(full_text)} characters total")
        
        return full_text
    
    except Exception as e:
        print(f"OCR extraction failed: {e}")
        return ""

def analyze_with_tfidf(text: str, n_clusters: int = 10):
    """
    Analyze text using TF-IDF to identify important terms and topics
    """
    print("Analyzing text with TF-IDF...")
    
    # Split text into sentences for analysis
    sentences = sent_tokenize(text)
    if len(sentences) < 10:
        print("Not enough sentences for meaningful TF-IDF analysis")
        return text, []
    
    # Prepare stopwords
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    
    # Custom stopwords for license documents
    license_stopwords = {'page', 'section', 'chapter', 'figure', 'table', 'see', 'also'}
    stop_words.update(license_stopwords)
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=1000,
        min_df=2,
        max_df=0.8,
        stop_words=list(stop_words),
        ngram_range=(1, 2),  # Include bigrams
        lowercase=True
    )
    
    try:
        # Fit and transform the sentences
        tfidf_matrix = vectorizer.fit_transform(sentences)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get top terms by TF-IDF score
        feature_scores = np.mean(tfidf_matrix.toarray(), axis=0)
        top_indices = np.argsort(feature_scores)[::-1][:50]  # Top 50 terms
        
        important_terms = [feature_names[i] for i in top_indices]
        print(f"Top TF-IDF terms: {important_terms[:20]}")
        
        # Cluster sentences to identify topics
        if len(sentences) >= n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            sentence_clusters = kmeans.fit_predict(tfidf_matrix)
            
            # Group sentences by cluster and prioritize based on TF-IDF scores
            clustered_text = []
            for cluster_id in range(n_clusters):
                cluster_sentences = [sentences[i] for i in range(len(sentences)) if sentence_clusters[i] == cluster_id]
                if cluster_sentences:
                    clustered_text.extend(cluster_sentences)
                    clustered_text.append("")  # Add separator between clusters
            
            organized_text = "\n".join(clustered_text)
        else:
            organized_text = text
        
        return organized_text, important_terms
        
    except Exception as e:
        print(f"TF-IDF analysis failed: {e}")
        return text, []

def create_smart_chunks(text: str, important_terms: list, chunk_size: int = 1200, chunk_overlap: int = 200):
    """
    Create chunks that preserve important terms and context
    """
    print("Creating smart chunks with TF-IDF guidance...")
    
    # Create custom separators that preserve important contexts
    separators = ["\n\n", "\n", ". ", "? ", "! ", "; ", " "]
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=separators
    )
    
    chunks = splitter.split_text(text)
    
    # Score chunks based on important terms
    scored_chunks = []
    for chunk in chunks:
        if not chunk.strip():
            continue
            
        chunk_lower = chunk.lower()
        
        # Calculate importance score based on TF-IDF terms
        importance_score = 0
        for term in important_terms[:20]:  # Use top 20 terms
            if term.lower() in chunk_lower:
                importance_score += 1
        
        # Boost score for license-related keywords
        license_keywords = ['license', 'licence', 'g1', 'g2', 'test', 'drive', 'permit', 'ontario', 'ministry', 'transport']
        for keyword in license_keywords:
            if keyword in chunk_lower:
                importance_score += 2
        
        scored_chunks.append((chunk, importance_score))
    
    # Sort by importance and create documents
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    
    # Keep all chunks but prioritize important ones
    documents = []
    for i, (chunk, score) in enumerate(scored_chunks):
        # Add metadata about importance
        metadata = {
            "importance_score": score,
            "chunk_index": i,
            "contains_license_terms": any(term in chunk.lower() for term in ['license', 'licence', 'g1', 'g2'])
        }
        documents.append(Document(page_content=chunk, metadata=metadata))
    
    print(f"Created {len(documents)} smart chunks with TF-IDF scoring")
    return documents

def main():
    # Check if OpenAI API key is available
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        sys.exit(1)
    
    pdf_path = "data/mto_drive.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        sys.exit(1)
    
    print("Extracting text from PDF using enhanced OCR...")
    text = extract_text_with_ocr(pdf_path, max_pages=30)  # Process first 30 pages
    
    if not text.strip():
        print("Error: No readable text could be extracted from PDF")
        sys.exit(1)
    
    print(f"\nExtracted {len(text)} characters of text")
    
    # Analyze with TF-IDF
    organized_text, important_terms = analyze_with_tfidf(text)
    
    # Check if we have license-related content
    text_lower = organized_text.lower()
    license_keywords = ['license', 'licence', 'g1', 'g2', 'drive', 'test', 'permit', 'ontario', 'handbook', 'ministry', 'transport']
    found_keywords = [kw for kw in license_keywords if kw in text_lower]
    print(f"Found license-related keywords: {found_keywords}")
    
    # Create smart chunks using TF-IDF insights
    documents = create_smart_chunks(organized_text, important_terms)
    
    # Show sample chunks
    print(f"\nTop 5 most important chunks:")
    for i in range(min(5, len(documents))):
        chunk_preview = documents[i].page_content[:200].replace('\n', ' ')
        score = documents[i].metadata.get('importance_score', 0)
        print(f"Chunk {i+1} (score: {score}): {chunk_preview}...")
    
    print("\nCreating embeddings and vector store...")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    print("Saving vector store...")
    vectorstore.save_local("vectorstore")
    
    print("✅ Vector store rebuilt successfully with OCR + TF-IDF!")
    
    # Test the retrieval
    print("\nTesting retrieval...")
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    test_docs = retriever.invoke("how do i get my g1 license?")
    
    for i, doc in enumerate(test_docs):
        content_preview = doc.page_content[:200].replace('\n', ' ')
        score = doc.metadata.get('importance_score', 0)
        print(f"Retrieved doc {i} (score: {score}): {content_preview}...")

if __name__ == "__main__":
    main() 