from app.config.cosmos import CosmosDB,policies_container,policy_premium_breakup_container,policy_addon_container,policy_benefit_container,policy_idv_breakup_container,policy_sections_container,vechile_details_container,policy_insured_members_container


class PolicyController:
    def __init__(self):
        pass

    def get_policy_details(self, policy_id: str):
        # Logic to retrieve policy details from Cosmos DB using the policy_id
        policy_details ={}
        
        policy_info = CosmosDB(policies_container).read_item(item_id=policy_id, partition_key=policy_id)
        
        if  not policy_info:
            raise Exception(f"Policy with id {policy_id} not found")
        
        policy_details["policy"] =policy_info
        insured_members = CosmosDB(policy_insured_members_container).read_all_items()
        benefits = CosmosDB(policy_benefit_container).read_all_items()
        sections = CosmosDB(policy_sections_container).read_all_items()
        vechile_details = CosmosDB(vechile_details_container).read_all_items()  
        idv_breakup = CosmosDB(policy_idv_breakup_container).read_all_items()
        premium_breakup = CosmosDB(policy_premium_breakup_container).read_all_items()   
        add_ons = CosmosDB(policy_addon_container).read_all_items()
        policy_details["insured_members"] = insured_members
        policy_details["benefits"] = benefits
        policy_details["sections"] = sections
        policy_details["vechile_details"] = vechile_details
        policy_details["idv_breakup"] = idv_breakup
        policy_details["premium_breakup"] = premium_breakup
        policy_details["add_ons"] = add_ons
        return policy_details
    

policy_controller = PolicyController()