
import logging

from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)
import tempfile


class TokenizationService():
    def __init__(self):
        pass            
    async def tokenize_files(self,raw_files):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunked_docs =[]
            for item in raw_files:
                content = item.file.read()
                tmp_path = None
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                    tmp.write(content)
                    tmp_path = tmp.name

                loader = UnstructuredWordDocumentLoader(tmp_path)
                documents = loader.load()

                logger.info(f"Processing file: {item.filename}")

                loader = UnstructuredWordDocumentLoader(tmp_path)
                documents = loader.load()
                texts = text_splitter.split_documents(documents)
                chunked_docs.extend(texts)
                logger.info(f"File {item.filename} tokenized into {len(texts)} chunks.")
            return chunked_docs
        except Exception as e:
            logger.error(f"Error in tokenization: {str(e)}")
            raise Exception(f"Tokenization Service failed: {str(e)}")


tokenize_service = TokenizationService()