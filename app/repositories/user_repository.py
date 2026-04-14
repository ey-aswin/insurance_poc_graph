from app.config.cosmos import CosmosDB,get_cosmos,container_info

db = CosmosDB(container_info[2])

class UserRepository:
    def __init__(self, ):
        self.db = db

    def get_user_by_id(self, user_id):
        # Implement logic to retrieve a user by ID from the database
        return self.db.read_item(item_id=user_id, partition_key=user_id)

    def create_user(self, user_data):
        # Implement logic to create a new user in the database
        self.db.create_item(item=user_data)

    def update_user(self, user_id, user_data):
        # Implement logic to update an existing user in the database
        self.db.update_item(item_id=user_id, partition_key=user_id, item=user_data)
        return self.db.read_item(item_id=user_id, partition_key=user_id)
    
    def delete_user(self, user_id):
        # Implement logic to delete a user from the database
        self.db.delete_item(item_id=user_id, partition_key=user_id)
        return {"message": f"User with ID {user_id} has been deleted."}
    