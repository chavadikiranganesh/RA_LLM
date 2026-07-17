from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def extract_text(pdf_file):
    """
    Read text from uploaded PDF.
    """

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def split_text(text):
    """
    Split text into chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_text(text)


def create_vector_store(chunks):
    """
    Create FAISS Vector Database.
    """

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embedding_model
    )

    return vector_store


def process_pdf(pdf_file):
    """
    Complete PDF processing pipeline.
    """

    text = extract_text(pdf_file)

    chunks = split_text(text)

    vector_store = create_vector_store(chunks)

    return vector_store