from app.config.cosmos import CosmosDB,get_cosmos,container_info


class CosmosContainerRepository:
    def __init__(self,db) :
        self.db = db

    def get_item_by_id(self, item_id:str):
        # Implement logic to retrieve an item by ID from the database
        return self.db.read_item(item_id=item_id, partition_key=item_id)
    
    def create_item(self, item: dict):
        # Implement logic to create a new item in the database
        self.db.create_item(item=item)
        
    def update_item(self, item_id: str, item_data: dict):
        # Implement logic to update an existing item in the database
        self.db.update_item(item_id=item_id, partition_key=item_id, item=item_data)
        return self.db.read_item(item_id=item_id, partition_key=item_id)
    
    def delete_item(self, item_id: str):
        # Implement logic to delete an item from the database
        self.db.delete_item(item_id=item_id, partition_key=item_id)
        return {"message": f"Item with ID {item_id} has been deleted."}
    
    def get_all_items(self):
        # Implement logic to retrieve all items from the database
        return self.db.read_all_items()
    
    def query_items(self, query: str):
        # Implement logic to query items from the database based on specific criteria
        return self.db.query_items(query=query)