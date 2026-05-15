import os
# import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.indexes import VectorstoreIndexCreator
from langchain_aws import ChatBedrock

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# _logger = logging.getLogger('vector_store_aws')
# _logger.setLevel(logging.INFO)
# if not _logger.handlers:
#     _fh = logging.FileHandler(os.path.join(_BASE_DIR, 'vector_data_aws.log'), encoding='utf-8')
#     _fh.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
#     _logger.addHandler(_fh)

# def _log_vector_store(db_index):
#     faiss_index      = db_index.vectorstore.index
#     id_map           = db_index.vectorstore.index_to_docstore_id
#     docstore         = db_index.vectorstore.docstore._dict
#     n                = faiss_index.ntotal
#     dim              = faiss_index.d
#
#     _logger.info("=" * 60)
#     _logger.info(f"Total chunks: {n}  |  Embedding dimensions: {dim}")
#     _logger.info("=" * 60)
#
#     for i in range(n):
#         doc_id  = id_map[i]
#         doc     = docstore[doc_id]
#         vector  = faiss_index.reconstruct(i)
#
#         _logger.info(f"--- Chunk {i+1:03d} ---")
#         _logger.info(f"  Doc ID   : {doc_id}")
#         _logger.info(f"  Metadata : {doc.metadata}")
#         _logger.info(f"  Text     : {doc.page_content}")
#         _logger.info(f"  Dims     : {len(vector)}")
#         _logger.info(f"  Vector   : {vector.tolist()}")
#
#     _logger.info("=" * 60)

def hr_index():
    data_load = PyPDFLoader(os.path.join(_BASE_DIR, 'LeavePolicy-2026.pdf'))
    data_split = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=100, chunk_overlap=10)
    data_embeddings = BedrockEmbeddings(
        credentials_profile_name='default',
        model_id='amazon.titan-embed-text-v2:0')
    data_index = VectorstoreIndexCreator(
        text_splitter=data_split,
        embedding=data_embeddings,
        vectorstore_cls=FAISS)
    db_index = data_index.from_loaders([data_load])
    return db_index

def hr_llm():
    llm = ChatBedrock(
        credentials_profile_name='default',
        model_id='us.amazon.nova-micro-v1:0',
        model_kwargs={
            "max_tokens": 500,
            "temperature": 0.1,
            "top_p": 0.9})
    return llm

def hr_rag_response(index, question):
    rag_llm = hr_llm()
    return index.query(question=question, llm=rag_llm)
