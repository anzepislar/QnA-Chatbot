import os
from dotenv import load_dotenv
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
pinecone_key = os.getenv("PINECONE_API_KEY")

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters.markdown import MarkdownHeaderTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from pathlib import Path

def main(question: str, file_path: str):
    """Run RAG over a single document provided explicitly by file_path."""

    if not file_path:
        raise ValueError("file_path must be provided explicitly.")

    file_path = str(file_path)

    # Loader auto-detect (works even if the temp file path has no extension)
    pages = None
    last_err = None

    for try_loader in (
        lambda p: PyPDFLoader(p).load(),
        lambda p: Docx2txtLoader(p).load(),
        lambda p: TextLoader(p, encoding="utf-8").load(),
    ):
        try:
            pages = try_loader(file_path)
            last_err = None
            break
        except Exception as e:
            last_err = e

    if pages is None:
        raise TypeError(
            f"Could not load file at '{file_path}'. Supported: PDF, DOCX, TXT. "
            f"Last error: {last_err}"
        )
        
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Title 1"),
            ("##", "Title 2"),
            ("###", "Title 3"),
        ]
    )

    pages_md = md_splitter.split_text(pages[0].page_content)

    char_splitter = CharacterTextSplitter(
        separator=".",
        chunk_size=700,
        chunk_overlap=150,
        length_function=len,
    )

    pages_char = char_splitter.split_documents(pages_md)

    emb_ada = OpenAIEmbeddings(model='text-embedding-3-small')

    # PINECONE
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    index_name = 'rag-chatbot'
    DIM = 1536

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            vector_type='dense',
            dimension=DIM,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )

    index = pc.Index(index_name)

    texts = [d.page_content for d in pages_char]
    vectors = emb_ada.embed_documents(texts)

    to_upsert = []
    for i, (vec, doc) in enumerate(zip(vectors, pages_char)):
        meta = dict(doc.metadata) if doc.metadata else {}
        meta["text"] = doc.page_content  # <-- this is basically your text_key
        to_upsert.append((f"chunk-{i}", vec, meta))

    index.upsert(vectors=to_upsert, namespace="client-a")

    TEMPLATE = '''
    Answer the following question:
    {question}

    To answer the question, use only the following context:
    {context}

    At the end, include the title of the section where you got the information from:
    Resources: *Section Title*
    '''

    prompt_template = PromptTemplate.from_template(TEMPLATE)

    chat = ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0,
        streaming=True
        )

    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    def retriever(question: str, k: int=3, namespace: str='client-a'):
        qvec = emb_ada.embed_query(question)
        
        res = index.query(
            vector=qvec,
            top_k=k,
            include_metadata=True,
            namespace=namespace
        )
        
        docs = []
        for m in res.get('matches', []):
            md = m.get('metadata') or {}
            text = md.get('text', '')
            docs.append(Document(page_content=text, metadata=md))
            
        return docs

    retriever_r = RunnableLambda(lambda q: retriever(q, k=3))
    chain = ({'context': retriever_r | format_docs, 'question': RunnablePassthrough()} | prompt_template | chat | StrOutputParser())

    return chain.invoke(question)
