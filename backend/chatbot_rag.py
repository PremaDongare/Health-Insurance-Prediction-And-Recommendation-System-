import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import pickle
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("Google_Gemani_API"))  # Configure Gemini API Key

ROBOTS_URL = "https://www.sbigeneral.in/robots.txt"
rp = RobotFileParser()
rp.set_url(ROBOTS_URL)
rp.read()


# ------------------- SCRAPER -------------------
def scrape_glossary():
    base_url = "https://www.sbigeneral.in/health-insurance/glossary/"
    all_text = ""
    if rp.can_fetch("*", base_url):
        try:
            response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            all_text += soup.get_text(separator="\n")
        except requests.exceptions.RequestException as e:
            print(f"Skipping main glossary page due to error: {e}")
    else:
        print("Main glossary page disallowed by robots.txt")

    for letter in "abcdefghijklmnopqrstuvwxyz":
        url = f"{base_url}{letter}"
        if rp.can_fetch("*", url):
            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                all_text += "\n" + soup.get_text(separator="\n")
                time.sleep(1)  # polite delay
            except requests.exceptions.RequestException as e:
                print(f"Skipping {url} due to error: {e}")
        else:
            print(f"Skipping {url} as disallowed in robots.txt")
    return all_text


# ------------------- TEXT SPLITTING -------------------
def split_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    return chunks


# ------------------- VECTORSTORE -------------------
def get_vectorstore(chunks, path="vectorstore.pkl"):
    if os.path.exists(path):
        print("Loading cached vectorstore...")
        with open(path, "rb") as f:
            vectorstore = pickle.load(f)
    else:
        print("Creating vectorstore...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_texts(chunks, embeddings)
        with open(path, "wb") as f:
            pickle.dump(vectorstore, f)
    return vectorstore


# ------------------- RETRIEVAL -------------------
def retrieve_relevant_chunks(vectorstore, query, k=5):
    results = vectorstore.similarity_search(query, k=k)
    return " ".join([r.page_content for r in results])


# ------------------- GEMINI ASK -------------------
def ask_gemini(context, query, simplify=False):
    if simplify:
        prompt = f"""
        You are a teacher. Explain the following in **very simple and easy words** 
        as if talking to a beginner, with a small real-life example if possible.

        Context: {context}

        Question: {query}

        Simplified Answer:
        """
    else:
        prompt = f"""
        Context: {context}

        Question: {query}

        Answer concisely:
        """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Sorry, I encountered an error while processing your question. Please try again."


def get_answer_from_gemini(query):
    try:
        glossary_cache = "glossary.txt"
        if os.path.exists(glossary_cache):
            with open(glossary_cache, "r", encoding="utf-8") as f:
                glossary_text = f.read()
        else:
            glossary_text = scrape_glossary()
            with open(glossary_cache, "w", encoding="utf-8") as f:
                f.write(glossary_text)

        chunks = split_text(glossary_text)
        vectorstore = get_vectorstore(chunks)
        relevant_context = retrieve_relevant_chunks(vectorstore, query)

        # Detect if user asked for "simple/easy" explanation
        simplify_keywords = ["simple", "easy", "beginner", "explain like", "in simple words"]
        simplify = any(word in query.lower() for word in simplify_keywords)

        # Step 1: Just return a message if query asks for registration / scheme link
        if any(word in query.lower() for word in ["register", "apply", "buy policy", "link", "portal", "scheme"]):
            return "For registration or scheme links, please visit the official insurance provider’s website."

        # Step 2: Use glossary vectorstore if relevant context is found
        if relevant_context and len(relevant_context.strip()) > 50:
            return ask_gemini(relevant_context, query, simplify=simplify)

        #  Step 3: Otherwise, let Gemini answer from its own knowledge
        if "insurance" in query.lower() or "policy" in query.lower():
            return ask_gemini("", query, simplify=simplify)

        return "Sorry, I could not find relevant health insurance information."

    except Exception as e:
        print(f"Error in get_answer_from_gemini: {e}")
        return "Sorry, I encountered an error while processing your question. Please try again."
