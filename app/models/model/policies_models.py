import uuid

from pydantic import BaseModel, Field
from sqlalchemy import TIMESTAMP, UUID, VARCHAR, Enum, null


class PolicyTypeEnum(str, Enum):
    HEALTH = "HEALTH"
    MOTOR = "MOTOR"
    LIFE = "LIFE"
    TRAVEL = "TRAVEL"

# Basemodel for Policy, representing the "policies" table structure
class Policy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_type:PolicyTypeEnum
    user_id: str
    policy_number: str
    uin: str
    policy_type: str
    insurer_name: str
    product_name: str
    plan_variant: str
    coverage_amount: float
    auto_approval_limit: float
    deductible: float
    start_date: str
    end_date: str
    policy_status: str
    created_at: str
    policy_holder_name: str
    policy_holder_dob: str
    policy_holder_gender: str
    business_channel_code: str
    gstin: str
    broker_name: str
    broker_irda_license_no: str
    issuer_address: str
    issuer_helpline: str
    issuer_website: str
    qr_code_url: str
    irda_registration_no: str
    stamp_duty_paid: bool
    premium_base: float
    gst_amount: float
    premium_total: float
    moratorium_years: int
    motor_policy_type: str
    ncb_percent: float
    financier_name: str
    idv_total: float
    compulsory_deductible: float
    voluntary_deductible: float
    geographical_area: str
    
class PolicyPremiumBreakup(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_id: str
    od_base_premium: float
    od_addon_total: float
    tp_premium: float
    pa_owner_driver_premium: float
    pa_paid_driver_premium: float
    pa_unnamed_passengers_premium: float
    ncb_percent: float
    discount_ncb_amount: float
    discount_anti_theft_amount: float
    discount_aai_amount: float
    loading_geography_amount: float
    premium_subtotal: float
    gst_amount: float
    premium_total: float
    notes: str
    created_at: str

class PolicyAddon(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_id: str
    addon_name: str
    premium: float
    sum_insured: float
    limit_notes: str
    created_at: str
    
class PolicyBenefit(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_id: str
    benefit_name: str
    benefit_category: str
    description: str
    sublimit_type: str
    sublimit_value: float
    notes: str
    created_at: str
    
class PolicySections(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_id: str
    section_type: str
    title: str
    content: str
    created_at: str

class PolicyInsuredMembers(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_id: str
    member_name: str
    member_dob:str
    member_gender: str
    member_relationship: str
    created_at: str
    coverage_amount: float
    
    
class VechileDetails(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_id: str
    registration_number: str
    make_model_variant: str
    fuel_type: str
    year_of_manufacture: int
    cubic_capacity_cc: int
    seating_capacity: int
    engine_number: str
    chassis_number: str
    vechile_category: str
    registration_date: str
    created_at: str
    
class PolicyIDVBreakup(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_id: str
    idv_vechile: float
    idv_electrical_accessories: float
    idv_non_electrical_accessories: float
    idv_cng_lpg_kit: float
    idv_trailer: float
    idv_total: float
    coinsurance_percent: float
    coinsurance_amount: float   
    notes: str
    created_at: str