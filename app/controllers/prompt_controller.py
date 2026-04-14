import logging

from app.services.embedding_service import EmbeddingService
from app.services.neo4j_service import neo4j_service
from app.services.prompt_service import PromptService
from app.services.qdrant_service import QdrantService

logger = logging.getLogger(__name__)
class PromptController:
    def __init__(self):
        pass

    def generate_prompt(self, query: str,user_id:str="admin"):
        # Placeholder for prompt generation logic
        
        # Convert  the Query to Embeddings
        logger.info("Generating query embedding")
        embedding_service = EmbeddingService()
        query_embedding = embedding_service.generate_embeddings_for_query(query)
        logger.info("Query embedding generated successfully")
        
        # Use the Embeddings to retrieve relevant chunks from Qdrant
        logger.info("Searching for relevant chunks in Qdrant")
        qdrant_service = QdrantService()
        qdrant_search_results = qdrant_service.qdrant_search(q_emb=query_embedding, top_k=5)
        logger.info("Relevant chunks retrieved successfully from Qdrant")
        
        # Use the retrieved chunks to generate a prompt using LLM
        logger.info("Generating prompt using retrieved chunks")
        prompt_service = PromptService()
        prompt = prompt_service.generate_answer_from_hits(qdrant_search_results, query)
        logger.info("Prompt generated successfully")
        
        # return the generated prompt
        logger.info("Returning generated prompt...")
        return {"message": "Prompt generated successfully!", "prompt": prompt}
    
    def prompt_on_graph_from_embedding(self, session_id: str, query: str = "Which are the disease covered in the Insurance?"):
        
        
        # Convert the Query to Embeddings
        logger.info("Generating query embedding")
        embedding_service = EmbeddingService()
        query_embedding = embedding_service.generate_embedding_for_chunk(query)
        logger.info("Query embedding generated successfully")
        
        # Reterive the graph data from Neo4j using the session_id and query
        logger.info("Retrieving graph data from Neo4j")
        prompt_service = PromptService()
        graph_data =neo4j_service.retrieve_graph_data(session_id=session_id, question=query, llm=prompt_service.get_llm())
        logger.info("Graph data retrieved successfully from Neo4j")
        logger.info("Graph Data: %s", str(graph_data))
        
        
        # Reterive the relevant chunks from Neo4j Embeddings using the query embedding and session_id   
        logger.info("Retrieving relevant chunks from Neo4j using query embedding")
        relevant_chunks = neo4j_service.retrieve_embeddings(session_id=session_id, question_embedding=query_embedding)
        logger.info("Relevant chunks retrieved successfully from Neo4j")
        # logger.info("Relevant Chunks: %s", relevant_chunks)
        
        # Use the retrieved graph data and chunks to generate a prompt using LLM
        logger.info("Generating prompt using retrieved graph data and chunks")
        prompt = prompt_service.final_response_parser_graph_and_embeddings(graph_data, relevant_chunks, question=query)
        logger.info("Prompt generated successfully from graph data and chunks")
        logger.info("Generated Prompt: %s", prompt)
        
        return {"message": "Prompt generated successfully from graph data!", "prompt": query, "response": prompt}
    
prompt_controller = PromptController()