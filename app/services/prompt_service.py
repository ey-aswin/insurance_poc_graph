

from cmd import PROMPT
from cmd import PROMPT
import json
import logging
import math
from typing import Any, Dict, List

from langchain_core import documents

from app.config import settings
from app.config.settings import settings
from app.models.schemas.schema import ChunkInfo, FileEmbeddingInfo, GraphData
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

logger = logging.getLogger(__name__)

question = "What is the coverage amount for the policy?"

import os

from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
deployment = "gpt-4o"
class PromptService:
    def __init__(self):
        self.gpt_client = AzureOpenAI(
            api_version="2025-03-01-preview" ,
            # or settings.AZURE_OPENAI_PROMPT_API_VERSION
            azure_endpoint=settings.AZURE_OPENAI_PROMPT_ENDPOINT,
            api_key=settings.AZURE_OPENAI_PROMPT_API_KEY,
            # deployment=settings.AZURE_OPENAI_PROMPT_DEPLOYMENT
        )
        
    def get_llm(self):
        return  AzureChatOpenAI(
            api_version="2025-03-01-preview",
            azure_endpoint=settings.AZURE_OPENAI_PROMPT_ENDPOINT,
            api_key=settings.AZURE_OPENAI_PROMPT_API_KEY,
            azure_deployment=deployment,
        )


    async def extract_graph_from_text(self, embedding_info:list[FileEmbeddingInfo]):
        transformer = LLMGraphTransformer(
        llm=self.get_llm(),
        strict_mode=False,
        ignore_tool_usage=True,

    )
        input_texts = [Document(page_content=info.text) for info in embedding_info]
        raw_graph =await transformer.aconvert_to_graph_documents(input_texts)
        return raw_graph
    
    
    async def extract_graph_info(self, embedding_info:list[FileEmbeddingInfo]):
        print("Extracting graph info for embedding:", embedding_info)

        print("Processing embedding chunk:", embedding_info[0].chunk_id, embedding_info[0].text[:100])  # Log the chunk ID and a snippet of the text for debugging
        graph = await self.extract_graph_from_text(embedding_info)
       
        return graph
        

    def final_response_parser_graph_and_embeddings(self,graph_data,embedding_info,question):
        # IMPLEMENT THE LOGIC TO PARSE THE FINAL RESPONSE FROM THE LLM AND EXTRACT GRAPH DATA AND EMBEDDINGS
        try:
            PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful assistant that answers questions based on retrieved text chunks and graph database results.
    Use the following retrieved text chunks and graph results to answer the question. Be concise and accurate.
    Retrieved Text Chunks:
    {retrieved_chunks}
    Graph Results:
    {graph_results}
    User Question:
    {question}
    """
)

            chain = PROMPT | self.get_llm()
            # Print the retrieved chunks and graph results for debugging
            print("Embeddings",embedding_info)
            print("Graph Results", graph_data)

            output = chain.invoke({
                "retrieved_chunks": "\n".join([f"- {res['text']} (score: {res['score']:.4f})" for res in embedding_info]),
                "graph_results": graph_data,
                "question": question
            })
            # print(output)
            return output.content

        except Exception as e:
            logger.exception("Error parsing final response")
            raise Exception(f"Final response parsing failed: {str(e)}")