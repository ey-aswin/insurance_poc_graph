from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
   app_name: str = "Awesome API"
   COSMOS_DB_CREDENTIAL: str
   DATABASE_NAME: str
   
   AZURE_OPENAI_ENDPOINT:str
   AZURE_OPENAI_MODEL_NAME: str
   AZURE_OPENAI_DEPLOYMENT: str
   AZURE_OPENAI_API_VERSION: str
   AZURE_OPENAI_API_KEY: str

   # Vector dimension must match your embedding model output length.
   # Defaults to 3072 (e.g. text-embedding-3-large). Override via .env if needed.
   AZURE_OPENAI_EMBEDDING_DIMENSIONS: int = 3072
   
   # QDRANT_URL: str
   
   AZURE_OPENAI_PROMPT_ENDPOINT: str
   AZURE_OPENAI_PROMPT_MODEL_NAME: str
   AZURE_OPENAI_PROMPT_DEPLOYMENT: str
   AZURE_OPENAI_PROMPT_API_KEY: str
   AZURE_OPENAI_PROMPT_API_VERSION: str
   
   NEO4J_URI: str
   NEO4J_USER: str
   NEO4J_PASSWORD: str

   # Neo4j driver connection tuning (helps avoid failures after long idle)
   # All values are in seconds unless noted otherwise.
   NEO4J_KEEP_ALIVE: bool = True
   NEO4J_LIVENESS_CHECK_TIMEOUT: int = 5
   # Force pooled connections to be recycled before common cloud idle timeouts (e.g., ~10 min).
   NEO4J_MAX_CONNECTION_LIFETIME: int = 540
   NEO4J_CONNECTION_TIMEOUT: int = 15
   NEO4J_CONNECTION_ACQUISITION_TIMEOUT: int = 30
   NEO4J_MAX_CONNECTION_POOL_SIZE: int = 50
   
   # Cosmos DB settings
   COSMOS_USERS_CONTAINER: str = "users"
   COSMOS_USERS_PROFILE_CONTAINER: str = "user_profiles"
   COSMOS_AUDIT_LOGS_CONTAINER: str = "audit_logs"
   COSMOS_POLICIES_CONTAINER: str = "policies"
   COSMOS_POLICY_PREMIUM_BREAKUP_CONTAINER: str = "policy_premium_breakup"
   COSMOS_POLICY_ADDON_CONTAINER: str = "policy_addon"
   COSMOS_POLICY_BENEFIT_CONTAINER: str = "policy_benefit"
   COSMOS_POLICY_IDV_BREAKUP_CONTAINER: str = "policy_idv_breakup"
   COSMOS_POLICY_SECTIONS_CONTAINER: str = "policy_sections"
   COSMOS_POLICY_INSURED_MEMBERS_CONTAINER: str = "policy_insured_members"
   COSMOS_VECHILE_DETAILS_CONTAINER: str = "vechile_details"
   COSMOS_CLAIMS_CONTAINER: str  = "claims"
   COSMOS_CLAIM_DOCUMENTS_CONTAINER: str= "claim_documents"
   COSMOS_CLAIM_DOCUMENT_EXTRACTION_RESULTS_CONTAINER: str = "claim_document_extraction_results"
   COSMOS_CLAIM_STATUS_HISTORY_CONTAINER: str = "claim_status_history"
   COSMOS_CLAIM_RULES_CONTAINER: str = "claim_rules"
   COSMOS_APPROVAL_OVERRIDES_CONTAINER: str = "approval_overrides"
   COSMOS_CLAIM_APPROVALS_CONTAINER: str = "claim_approvals"
   COSMOS_CLAIM_ASSIGNMENTS_CONTAINER: str = "claim_assignments"
   COSMOS_CLAIM_RULE_EVALUATIONS_CONTAINER: str = "claim_rule_evaluations"
   COSMOS_CHAT_SESSIONS_CONTAINER: str = "chat_sessions"
   COSMOS_CHAT_MESSAGES_CONTAINER: str = "chat_messages"
   
   
   
   model_config = SettingsConfigDict(
        env_file=".env",     # local only
        case_sensitive=True # Azure Linux is case-sensitive
    )



settings = Settings()