from app.config.settings import settings
from app.utils.logger_utils import logger
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError


class CosmosDB:
    def __init__(self, CONNECTION_STRING: str, DATABASE_NAME: str, CONTAINER_NAME: str):
        client = CosmosClient.from_connection_string(CONNECTION_STRING)
        self.database = client.get_database_client(DATABASE_NAME)
        self.container = self.database.get_container_client(CONTAINER_NAME)
        
        self.database_name = DATABASE_NAME
        self.container_name = CONTAINER_NAME


    def create_item(self, item: dict):
        try:
            self.container.create_item(body=item)
            logger.info(f"Item created successfully in Cosmos DB container {self.container_name}")
        except Exception as e:
            logger.error(f"Error creating item in Cosmos DB: {e}")
            raise Exception(f"Failed to create item in Cosmos DB: {str(e)}")


    def read_item(self, item_id: str, partition_key: str):
        try:
            item = self.container.read_item(item=item_id, partition_key=partition_key)
            logger.info(f"Item read successfully from Cosmos DB container {self.container_name}")
            return item
        except CosmosResourceNotFoundError:
            logger.warning(f"Item {item_id} not found in Cosmos DB.")
            return None
        except Exception as e:
            logger.error(f"Error reading item from Cosmos DB: {e}")
            raise Exception(f"Failed to read item from Cosmos DB: {str(e)}")


    def read_all_items(self):
        try:
            items = list(self.container.query_items(
                query="SELECT * FROM c",
                enable_cross_partition_query=True
            ))
            logger.info(f"All items read successfully from Cosmos DB container {self.container_name}")
            return items
        except Exception as e:
            logger.error(f"Error reading all items from Cosmos DB: {e}")
            raise Exception(f"Failed to read all items from Cosmos DB: {str(e)}")


    def delete_item(self, item_id: str, partition_key: str):
        try:
            self.container.delete_item(item=item_id, partition_key=partition_key)
            logger.info(f"Item deleted successfully from Cosmos DB container {self.container_name}")
            return True
        except CosmosResourceNotFoundError:
            logger.warning(f"Item {item_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting item from Cosmos DB: {e}")
            raise Exception(f"Failed to delete item from Cosmos DB: {str(e)}")



def get_container(container_name: str):
    logger.info(f"Initializing Cosmos DB client for {container_name} container")
    logger.info(f"Using Cosmos DB database name: {settings.DATABASE_NAME}")

    return CosmosDB(
        CONNECTION_STRING=settings.COSMOS_DB_CREDENTIAL,
        DATABASE_NAME=settings.DATABASE_NAME,
        CONTAINER_NAME=container_name
    )