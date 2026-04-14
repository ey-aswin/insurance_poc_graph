import uuid

from pydantic import BaseModel, Field
from sqlalchemy import null


class Claim(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    user_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    claim_reference:str = Field(default_factory=lambda: str(uuid.uuid4()))
    claim_amount:float
    approved_amount:float
    incident_date:str
    claim_type:str
    description:str
    status:str = Field(default='DRAFT')
    priority:str
    sla_due_at:str 
    decision_summary:str
    rejection_reason:str
    created_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    updated_at:str = Field(default_factory=lambda: str(uuid.uuid4()))

class ClaimDocument(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    claim_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    file_name:str
    file_url:str
    document_type:str
    uploaded_by:str
    created_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    updated_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    
class ClaimDocumentExtractionResult(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    claim_document_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    extracted_field:dict
    confidence_score:float
    is_valid:bool
    created_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    updated_at:str = Field(default_factory=lambda: str(uuid.uuid4()))    
    
class ClaimStatusHistory(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    claim_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    from_status:str
    to_status:str
    changed_by:str
    reason:str
    created_at:str = Field(default_factory=lambda: str(uuid.uuid4()))   
    changed_at:str = Field(default_factory=lambda: str(uuid.uuid4()))


class ClaimRules(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    policy_type:str
    rule_name:str
    rule_category:str
    condition:str
    outcome:str
    priority:int
    active:bool
    created_at:str = Field(default_factory=lambda: str(uuid.uuid4()))

class ClaimRuleEvaluation(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    claim_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    rule_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    evaluation_result:str
    explanation:str
    evaluated_by:str
    evaluated_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
     
class ClaimAssignment(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    claim_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    assigned_to:str
    assigned_by:str
    assignment_reason:str
    created_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    updated_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    
class ClaimApproval(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    claim_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    approved_by:str
    approval_decision:str
    approved_amount:float
    approval_notes:str
    created_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    updated_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    
class ApprovalOverride(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid.uuid4())) 
    claim_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    overridden_by:str
    override_reason:str
    rule_id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    new_approved_amount:float
    created_at:str = Field(default_factory=lambda: str(uuid.uuid4()))
    updated_at:str = Field(default_factory=lambda: str(uuid.uuid4()))