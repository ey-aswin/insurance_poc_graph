from azure.cosmos import CosmosClient, PartitionKey, exceptions
from app.config.settings import settings
from app.models.model.user_models import User,UserProfile,AuditLogs
from app.models.model.policies_models import Policy,PolicyPremiumBreakup,PolicyAddon,PolicyBenefit,PolicyIDVBreakup,PolicySections,PolicyInsuredMembers,VechileDetails
from app.models.model.chat_model import ChatSession,ChatMessage
from app.models.model.claim_model import Claim,ClaimDocument,ClaimDocumentExtractionResult,ClaimStatusHistory,ClaimRules,ApprovalOverride,ClaimApproval,ClaimAssignment,ClaimRuleEvaluation

client = None
db = None

users_container = None
users_profile_container = None
audit_logs_container = None

policies_container = None
policy_premium_breakup_container = None
policy_addon_container = None
policy_benefit_container = None
policy_idv_breakup_container = None
policy_sections_container = None
policy_insured_members_container = None
vechile_details_container = None

claims_container = None
claim_documents_container = None
claim_document_extraction_results_container = None
claim_status_history_container = None
claim_rules_container = None
approval_overrides_container = None
claim_approvals_container = None
claim_assignments_container = None
claim_rule_evaluations_container = None

chat_sessions_container = None
chat_messages_container = None

def get_cosmos():
    global client, db, users_container, users_profile_container, audit_logs_container,policies_container,policy_premium_breakup_container,policy_addon_container,policy_benefit_container,policy_idv_breakup_container,policy_sections_container,policy_insured_members_container,vechile_details_container,claims_container,claim_documents_container,claim_document_extraction_results_container,claim_status_history_container,claim_rules_container,approval_overrides_container,claim_approvals_container,claim_assignments_container,claim_rule_evaluations_container,chat_sessions_container,chat_messages_container,policy_sections_container,policy_insured_members_container,vechile_details_container
    if client:
        return client, db, users_container, users_profile_container, audit_logs_container,policies_container,policy_premium_breakup_container,policy_addon_container,policy_benefit_container,policy_idv_breakup_container,policy_sections_container,policy_insured_members_container,vechile_details_container,claims_container,claim_documents_container,claim_document_extraction_results_container,claim_status_history_container,claim_rules_container,approval_overrides_container,claim_approvals_container,claim_assignments_container,claim_rule_evaluations_container,chat_sessions_container,chat_messages_container,policy_sections_container,policy_insured_members_container,vechile_details_container
    client = CosmosClient.from_connection_string(settings.COSMOS_DB_CREDENTIAL)
    db = client.create_database_if_not_exists(id=settings.DATABASE_NAME)

    
    users_container = db.create_container_if_not_exists(id=settings.COSMOS_USERS_CONTAINER, partition_key=PartitionKey(path="/id"))
    users_profile_container = db.create_container_if_not_exists(id=settings.COSMOS_USERS_PROFILE_CONTAINER, partition_key=PartitionKey(path="/id"))
    audit_logs_container = db.create_container_if_not_exists(id=settings.COSMOS_AUDIT_LOGS_CONTAINER, partition_key=PartitionKey(path="/id"))   
    policies_container = db.create_container_if_not_exists(id=settings.COSMOS_POLICIES_CONTAINER, partition_key=PartitionKey(path="/id"))
    policy_premium_breakup_container = db.create_container_if_not_exists(id=settings.COSMOS_POLICY_PREMIUM_BREAKUP_CONTAINER, partition_key=PartitionKey(path="/id"))
    policy_addon_container = db.create_container_if_not_exists(id=settings.COSMOS_POLICY_ADDON_CONTAINER, partition_key=PartitionKey(path="/id"))
    policy_benefit_container = db.create_container_if_not_exists(id=settings.COSMOS_POLICY_BENEFIT_CONTAINER, partition_key=PartitionKey(path="/id"))
    policy_idv_breakup_container = db.create_container_if_not_exists(id=settings.COSMOS_POLICY_IDV_BREAKUP_CONTAINER, partition_key=PartitionKey(path="/id"))
    policy_sections_container = db.create_container_if_not_exists(id=settings.COSMOS_POLICY_SECTIONS_CONTAINER, partition_key=PartitionKey(path="/id"))
    policy_insured_members_container = db.create_container_if_not_exists(id=settings.COSMOS_POLICY_INSURED_MEMBERS_CONTAINER, partition_key=PartitionKey(path="/id"))
    vechile_details_container = db.create_container_if_not_exists(id=settings.COSMOS_VECHILE_DETAILS_CONTAINER, partition_key=PartitionKey(path="/id"))
    claims_container = db.create_container_if_not_exists(id=settings.COSMOS_CLAIMS_CONTAINER, partition_key=PartitionKey(path="/id"))
    claim_documents_container = db.create_container_if_not_exists(id=settings.COSMOS_CLAIM_DOCUMENTS_CONTAINER, partition_key=PartitionKey(path="/id"))
    claim_document_extraction_results_container = db.create_container_if_not_exists(id=settings.COSMOS_CLAIM_DOCUMENT_EXTRACTION_RESULTS_CONTAINER, partition_key=PartitionKey(path="/id"))
    claim_status_history_container = db.create_container_if_not_exists(id=settings.COSMOS_CLAIM_STATUS_HISTORY_CONTAINER, partition_key=PartitionKey(path="/id"))
    claim_rules_container = db.create_container_if_not_exists(id=settings.COSMOS_CLAIM_RULES_CONTAINER, partition_key=PartitionKey(path="/id"))
    approval_overrides_container = db.create_container_if_not_exists(id=settings.COSMOS_APPROVAL_OVERRIDES_CONTAINER, partition_key=PartitionKey(path="/id"))
    claim_approvals_container = db.create_container_if_not_exists(id=settings.COSMOS_CLAIM_APPROVALS_CONTAINER, partition_key=PartitionKey(path="/id"))
    claim_assignments_container = db.create_container_if_not_exists(id=settings.COSMOS_CLAIM_ASSIGNMENTS_CONTAINER, partition_key=PartitionKey(path="/id"))
    claim_rule_evaluations_container = db.create_container_if_not_exists(id=settings.COSMOS_CLAIM_RULE_EVALUATIONS_CONTAINER, partition_key=PartitionKey(path="/id"))
    chat_sessions_container = db.create_container_if_not_exists(id=settings.COSMOS_CHAT_SESSIONS_CONTAINER, partition_key=PartitionKey(path="/id"))
    chat_messages_container = db.create_container_if_not_exists(id=settings.COSMOS_CHAT_MESSAGES_CONTAINER, partition_key=PartitionKey(path="/id"))
    
    return client, db, users_container, users_profile_container, audit_logs_container,policies_container,policy_premium_breakup_container,policy_addon_container,policy_benefit_container,policy_idv_breakup_container,policy_sections_container,policy_insured_members_container,vechile_details_container,claims_container,claim_documents_container,claim_document_extraction_results_container,claim_status_history_container,claim_rules_container,approval_overrides_container,claim_approvals_container,claim_assignments_container,claim_rule_evaluations_container,chat_sessions_container,chat_messages_container,policy_sections_container,policy_insured_members_container,vechile_details_container

container_info = get_cosmos()

class CosmosDB:
    def __init__(self,container):
        self.container = container
    
    def create_item(self, item: dict):
        try:
            self.container.create_item(body=item)
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to create item in Cosmos DB: {str(e)}")
        
    def read_item(self, item_id: str, partition_key: str):
        try:
            item = self.container.read_item(item=item_id, partition_key=partition_key)
            return item
        except exceptions.CosmosResourceNotFoundError:
            return None
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to read item from Cosmos DB: {str(e)}")
        
    
    def read_item_by_other_key(self, key_name: str,key_value: str):
        query = f"SELECT * FROM c WHERE c.{key_name} = @{key_name}"
        print(f"Executing query: {query} with value: {key_value}")

        items = list(self.container.query_items(
            query=query,
            parameters=[
                {"name": f"@{key_name}", "value": key_value}
            ],
            enable_cross_partition_query=True
        ))

        return items

    #  i need to return only one item if there are multiple items matching the query, how can i do that?
    def read_one_item_by_other_key(self, key_name: str,key_value: str):
        query = f"SELECT * FROM c WHERE c.{key_name} = @{key_name} OFFSET 0 LIMIT 1"
        print(f"Executing query: {query} with value: {key_value}")
        items = list(self.container.query_items(
            query=query,
            parameters=[
                {"name": f"@{key_name}", "value": key_value}
            ],
            enable_cross_partition_query=True
        ))
        return items[0] if items else None


    
    def read_all_items(self):
        try:
            items = list(self.container.query_items(
                query="SELECT * FROM c",
                enable_cross_partition_query=True
            ))
            return items
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to read all items from Cosmos DB: {str(e)}")
        
    def delete_item(self, item_id: str, partition_key: str):
        try:
            self.container.delete_item(item=item_id, partition_key=partition_key)
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to delete item from Cosmos DB: {str(e)}")
        
        