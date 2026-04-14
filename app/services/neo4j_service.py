

import logging
import re
import threading

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, SessionExpired
import uuid
from app.config.settings import settings
from app.models.schemas.schema import FileEmbeddingInfo, GraphData

from langchain_neo4j import GraphCypherQAChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j import Neo4jGraph
logger = logging.getLogger(__name__)

def cypher_prompt():
    return ChatPromptTemplate.from_template(
        """
        You are a helpful assistant that generates Cypher queries based on the provided graph schema, 
        the user's question, and the active upload session.

    IMPORTANT FILTERING RULE:
    - All Cypher queries MUST only return nodes and relationships with:
        session_id = "{session_id}"
    - Every MATCH clause must include this filter.
    - If multiple variables are used, apply the filter to all of them.
    - NEVER return nodes or relationships from a different upload session.

    Graph Schema:
    {schema}

    User Question:
    {question}

    Generate a Cypher query that can be executed against the graph database
    to answer the user's question. Be concise and accurate.
    """
)


def clean_label(label: str) -> str:
    if not label:
        return "Entity"
    return re.sub(r"[^A-Za-z0-9_]", "_", label.replace(" ", "_"))


def _create_driver():
    return GraphDatabase.driver(
        uri=settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        keep_alive=getattr(settings, "NEO4J_KEEP_ALIVE", True),
        liveness_check_timeout=int(getattr(settings, "NEO4J_LIVENESS_CHECK_TIMEOUT", 5)),
        max_connection_lifetime=int(getattr(settings, "NEO4J_MAX_CONNECTION_LIFETIME", 540)),
        connection_timeout=int(getattr(settings, "NEO4J_CONNECTION_TIMEOUT", 15)),
        connection_acquisition_timeout=int(getattr(settings, "NEO4J_CONNECTION_ACQUISITION_TIMEOUT", 30)),
        max_connection_pool_size=int(getattr(settings, "NEO4J_MAX_CONNECTION_POOL_SIZE", 50)),
    )


driver = _create_driver()

# graph_driver = Neo4jGraph(driver=driver)


class Neo4jService:
    def __init__(self):
        self.driver =  _create_driver()
        self.create_indexes()  # Ensure indexes are created on initialization
        
    def create_indexes(self):
        try:
            with self.driver.session() as session:
                query = """
                    CREATE VECTOR INDEX embedding_vector_index IF NOT EXISTS
                    FOR (e:Embedding)
                    ON (e.vector)
                    OPTIONS {
                      indexConfig: {
                        `vector.dimensions`: 3072,
                        `vector.similarity_function`: 'cosine'
                      }
                    }
                """
                session.run(query)
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error(f"Neo4j service error: {str(e)}")
            raise Exception(f"Failed to create indexes in Neo4j: {str(e)}")

    def store_embeddings(self, embedding: list[FileEmbeddingInfo]):
        try:
            with self.driver.session() as session:
                logger.info(f"Starting to store embeddings")
                for embed in embedding:
                    chunk_id = embed.chunk_id
                    embedding_vector = embed.embedding
                    properties = embed.metadata
                    text = embed.text
                    session_id = embed.session_id
                    query = """
                        CREATE (e:Embedding {
                            chunk_id: $chunk_id,
                            vector: $embedding_vector,
                            text: $text,
                            session_id: $session_id
                        })
                        SET e += $properties
                    """
                    session.run(query, {"chunk_id": chunk_id, "embedding_vector": embedding_vector, "text": text, "session_id": session_id, "properties": properties})
                logger.info(f"Successfully stored embedding")
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error(f"Neo4j service error: {str(e)}")
            raise Exception(f"Failed to store embeddings in Neo4j: {str(e)}")
        
    def store_graph_data(self, graph, session_id: str):
        try:
            with self.driver.session() as session:
                logger.info(f"Starting to store graph data")
                query = """
                        MERGE (s:UploadSession {id: $session_id})
                        SET s.created_at = datetime()
                        """
                session.run(query, {"session_id": session_id})
                
                for item in graph:
                    # ✅ Insert Nodes
                    for node in item.nodes:
                    
                        node_id = node.id or str(uuid.uuid4())
                        source_text = item.source.page_content if item.source else "No source text available"

                        props = node.properties or {}
                        props["name"] = props.get("name", node.id)
                        props["description"] = props.get("description", source_text)

                        label = clean_label(node.type)

                        query = f"""
                        MERGE (n:{label} {{id: $id}})
                        SET n += $properties,
                            n.session_id = $session_id
                        WITH n
                        MATCH (s:UploadSession {{id: $session_id}})
                        MERGE (s)-[:HAS_NODE]->(n)
                        """

                        session.run(
                            query,
                            {
                                "id": node_id,
                                "properties": props,
                                "session_id": session_id
                            }
                        )

                    # ✅ Insert Relationships
                    for rel in item.relationships:              
                        
                        
                        source_id = rel.source.id
                        target_id = rel.target.id
                        rel_type = clean_label(rel.type)
                
                        query = f"""
                        MATCH (s {{id: $source_id}})
                        MATCH (t {{id: $target_id}})
                        MERGE (s)-[r:{rel_type}]->(t)
                        SET r += $properties,
                            r.session_id = $session_id
                        """
                
                        session.run(
                            query,
                            {
                                "source_id": source_id,
                                "target_id": target_id,
                                "properties": rel.properties or {},
                                "session_id": session_id
                            }
                        )  
                        logger.info(f"Successfully stored graph data")
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error(f"Neo4j service error: {str(e)}")
            raise Exception(f"Failed to store graph data in Neo4j: {str(e)}")

    def retrieve_embeddings(self, session_id: str, top_k: int = 5, question_embedding: list = None):
        try:
            logger.info(f"Starting to retrieve embeddings for session_id: {session_id} with top_k: {top_k}")
            with self.driver.session() as session:
                query = """
CALL db.index.vector.queryNodes(
  'embedding_vector_index',
  $top_k,
  $question_embedding
)
YIELD node, score
WHERE node.session_id = $session_id
RETURN node.text AS text, score
ORDER BY score DESC
"""
                result = session.run(query, {"session_id": session_id, "top_k": top_k, "question_embedding": question_embedding})
                logger.info(f"Successfully retrieved embeddings")
                logger.info(result)
                # return as "retrieved_chunks": "\n".join([f"- {res['text']} (score: {res['score']:.4f})" for res in embedding_info]),
                return [{"text": record["text"], "score": record["score"]} for record in result]
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error(f"Neo4j service error: {str(e)}")
            raise Exception(f"Failed to retrieve embeddings from Neo4j: {str(e)}")
        
    
    def get_schema_text(self, session_id: str):
        with self.driver.session() as session:

            # Node labels in this session
            labels = session.run(
                """
                MATCH (n {session_id: $session_id})
                UNWIND labels(n) AS label
                RETURN DISTINCT label
                """,
                {"session_id": session_id}
            ).value()
    
            # Relationship types in this session
            rels = session.run(
                """
                MATCH (a)-[r]->(b)
                WHERE a.session_id = $session_id OR b.session_id = $session_id
                RETURN DISTINCT type(r)
                """,
                {"session_id": session_id}
            ).value()
    
            # Property keys in this session
            props = session.run(
                """
                MATCH (n {session_id: $session_id})
                UNWIND keys(n) AS property
                RETURN DISTINCT property
                """,
                {"session_id": session_id}
            ).value()
    
            return (
                f"Node Labels: {labels}\n"
                f"Relationship Types: {rels}\n"
                f"Property Keys: {props}"
            )


    def retrieve_graph_data(self, session_id: str,question: str, llm):
        try:
            logger.info(f"Starting to retrieve graph data for session_id: {session_id}")
            with self.driver.session() as session:
                logger.info(f"Generating Cypher query using LLM for question: {question}")
                schema_text = self.get_schema_text(session_id)
                
                graph_driver =graph_driver = Neo4jGraph(
                    url=settings.NEO4J_URI,
                    username=settings.NEO4J_USER,
                    password=settings.NEO4J_PASSWORD,
                    )

                custom_cypher_prompt = cypher_prompt().partial(schema=schema_text,session_id=session_id)
                qa_chain = GraphCypherQAChain.from_llm(
                llm,
                graph=  graph_driver,
                verbose=True,
                allow_dangerous_requests=True,
                cypher_prompt=custom_cypher_prompt,
        )
                result = qa_chain.run(question)
                logger.info(f"Successfully retrieved graph data")
                # logger.info(result)
                # return as graph_results as str,
                return str(result)
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error(f"Neo4j service error: {str(e)}")
            raise Exception(f"Failed to retrieve graph data from Neo4j: {str(e)}")


def get_neo4j_service():
    return Neo4jService() 

neo4j_service = get_neo4j_service()