from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from enum import Enum


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    role: str  # patient, provider, family, guest
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserProfileCreate(BaseModel):
    name: str
    email: str
    role: str

class HealthMetric(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    metric_type: str  # weight, blood_pressure, calories, etc.
    value: float
    unit: str
    recorded_at: datetime = Field(default_factory=datetime.utcnow)

class HealthMetricCreate(BaseModel):
    user_id: str
    metric_type: str
    value: float
    unit: str

# ===== COMPREHENSIVE PROFILE MODELS =====

# Enums for Profile Data
class ActivityLevelEnum(str, Enum):
    SEDENTARY = "SEDENTARY"
    LIGHTLY_ACTIVE = "LIGHTLY_ACTIVE" 
    MODERATELY_ACTIVE = "MODERATELY_ACTIVE"
    VERY_ACTIVE = "VERY_ACTIVE"
    EXTRA_ACTIVE = "EXTRA_ACTIVE"

class WorkTypeEnum(str, Enum):
    DESK_JOB = "DESK_JOB"
    PHYSICAL_WORK = "PHYSICAL_WORK"
    MIXED = "MIXED"
    STUDENT = "STUDENT"
    RETIRED = "RETIRED"

class DietTypeEnum(str, Enum):
    OMNIVORE = "OMNIVORE"
    VEGETARIAN = "VEGETARIAN"
    VEGAN = "VEGAN"
    PESCATARIAN = "PESCATARIAN"
    FLEXITARIAN = "FLEXITARIAN"

class MealTimingEnum(str, Enum):
    TRADITIONAL_3_MEALS = "TRADITIONAL_3_MEALS"
    SMALL_FREQUENT = "SMALL_FREQUENT"
    INTERMITTENT_FASTING = "INTERMITTENT_FASTING"

# Patient Profile Models
class BasicInfo(BaseModel):
    full_name: str
    age: int
    gender: str
    location: str
    contact_preferences: Dict[str, bool] = {}
    timezone: str
    emergency_contact: Dict[str, str] = {}
    preferred_language: str = "English"

class PhysicalMetrics(BaseModel):
    height_cm: float
    current_weight_kg: float
    goal_weight_kg: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    measurements: Dict[str, float] = {}  # waist, chest, hips
    bmi: Optional[float] = None

class SleepSchedule(BaseModel):
    bedtime: str
    wake_time: str
    sleep_quality: int = Field(ge=1, le=5)

class ActivityProfile(BaseModel):
    activity_level: ActivityLevelEnum
    exercise_types: List[str] = []
    exercise_frequency: int  # days per week
    sleep_schedule: SleepSchedule
    stress_level: int = Field(ge=1, le=5)
    work_type: WorkTypeEnum

class HealthHistory(BaseModel):
    primary_health_goals: List[str] = []
    medical_conditions: Dict[str, str] = {}  # condition: severity
    current_medications: List[Dict[str, Any]] = []
    allergies: List[str] = []
    food_intolerances: List[str] = []
    previous_surgeries: List[Dict[str, Any]] = []
    family_medical_history: List[str] = []

class DietaryProfile(BaseModel):
    diet_type: DietTypeEnum
    cultural_restrictions: List[str] = []
    specific_diets: List[str] = []
    food_allergies: List[str] = []
    food_dislikes: List[str] = []
    meal_timing_preference: MealTimingEnum
    cooking_skill_level: int = Field(ge=1, le=5)
    available_cooking_time: int  # minutes per day

class GoalsPreferences(BaseModel):
    health_targets: List[Dict[str, Any]] = []
    communication_methods: List[str] = []
    notification_preferences: Dict[str, bool] = {}
    privacy_settings: Dict[str, bool] = {}
    data_sharing_preferences: Dict[str, bool] = {}

class PatientProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    role: str = "PATIENT"
    basic_info: Optional[BasicInfo] = None
    physical_metrics: Optional[PhysicalMetrics] = None
    activity_profile: Optional[ActivityProfile] = None
    health_history: Optional[HealthHistory] = None
    dietary_profile: Optional[DietaryProfile] = None
    goals_preferences: Optional[GoalsPreferences] = None
    profile_completion: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PatientProfileCreate(BaseModel):
    user_id: str
    basic_info: Optional[BasicInfo] = None
    physical_metrics: Optional[PhysicalMetrics] = None
    activity_profile: Optional[ActivityProfile] = None
    health_history: Optional[HealthHistory] = None
    dietary_profile: Optional[DietaryProfile] = None
    goals_preferences: Optional[GoalsPreferences] = None

class PatientProfileUpdate(BaseModel):
    basic_info: Optional[BasicInfo] = None
    physical_metrics: Optional[PhysicalMetrics] = None
    activity_profile: Optional[ActivityProfile] = None
    health_history: Optional[HealthHistory] = None
    dietary_profile: Optional[DietaryProfile] = None
    goals_preferences: Optional[GoalsPreferences] = None

# Provider Profile Models
class ProfessionalIdentity(BaseModel):
    full_name: str
    professional_title: str
    medical_license: str
    registration_numbers: Dict[str, str] = {}
    years_experience: int

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: int
    specialization: str

class Certification(BaseModel):
    name: str
    organization: str
    issue_date: str
    expiration_date: str
    status: str = "ACTIVE"

class ProfessionalCredentials(BaseModel):
    education: List[Education] = []
    certifications: List[Certification] = []
    specializations: List[str] = []

class PracticeInfo(BaseModel):
    workplace: str
    practice_type: str
    patient_demographics: List[str] = []
    languages_spoken: List[str] = []
    areas_of_expertise: List[str] = []

class WorkingHours(BaseModel):
    timezone: str
    schedule: Dict[str, Dict[str, str]] = {}  # day: {start, end}

class PracticePreferences(BaseModel):
    consultation_types: List[str] = []
    working_hours: WorkingHours
    max_patients: int
    accepting_new_patients: bool = True
    specialized_conditions: List[str] = []
    treatment_philosophies: List[str] = []

class ProviderProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    role: str = "PROVIDER"
    professional_identity: Optional[ProfessionalIdentity] = None
    credentials: Optional[ProfessionalCredentials] = None
    practice_info: Optional[PracticeInfo] = None
    preferences: Optional[PracticePreferences] = None
    verification_status: str = "PENDING"
    profile_completion: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProviderProfileCreate(BaseModel):
    user_id: str
    professional_identity: Optional[ProfessionalIdentity] = None
    credentials: Optional[ProfessionalCredentials] = None
    practice_info: Optional[PracticeInfo] = None
    preferences: Optional[PracticePreferences] = None

class ProviderProfileUpdate(BaseModel):
    professional_identity: Optional[ProfessionalIdentity] = None
    credentials: Optional[ProfessionalCredentials] = None
    practice_info: Optional[PracticeInfo] = None
    preferences: Optional[PracticePreferences] = None

# Family Profile Models
class FamilyStructure(BaseModel):
    family_role: str  # Parent, Spouse, Adult Child, etc.
    number_of_members: int
    primary_caregiver: bool = False

class FamilyMember(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    relationship: str
    age: int
    gender: str
    special_needs: List[str] = []
    allergies: List[str] = []
    medications: List[str] = []
    health_conditions: List[str] = []

class HouseholdManagement(BaseModel):
    common_dietary_restrictions: List[str] = []
    family_meal_preferences: List[str] = []
    budget_considerations: Dict[str, Any] = {}
    shopping_responsibilities: List[str] = []
    cooking_responsibilities: List[str] = []

class CareCoordination(BaseModel):
    healthcare_providers: Dict[str, Dict[str, str]] = {}  # member: {provider, contact}
    emergency_contacts: List[Dict[str, str]] = []
    medication_management: Dict[str, str] = {}
    health_tracking_preferences: Dict[str, bool] = {}

class FamilyProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    role: str = "FAMILY"
    family_structure: Optional[FamilyStructure] = None
    family_members: List[FamilyMember] = []
    household_management: Optional[HouseholdManagement] = None
    care_coordination: Optional[CareCoordination] = None
    profile_completion: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class FamilyProfileCreate(BaseModel):
    user_id: str
    family_structure: Optional[FamilyStructure] = None
    family_members: List[FamilyMember] = []
    household_management: Optional[HouseholdManagement] = None
    care_coordination: Optional[CareCoordination] = None

class FamilyProfileUpdate(BaseModel):
    family_structure: Optional[FamilyStructure] = None
    family_members: Optional[List[FamilyMember]] = None
    household_management: Optional[HouseholdManagement] = None
    care_coordination: Optional[CareCoordination] = None

# Guest Profile Models
class BasicDemographics(BaseModel):
    age: int
    gender: str
    activity_level: ActivityLevelEnum

class SimpleGoals(BaseModel):
    goal_type: str  # maintain, lose, gain
    target_amount: Optional[float] = None
    timeframe: Optional[str] = None

class GuestProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    role: str = "GUEST"
    basic_demographics: Optional[BasicDemographics] = None
    simple_goals: Optional[SimpleGoals] = None
    session_expires: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GuestProfileCreate(BaseModel):
    session_id: str
    basic_demographics: BasicDemographics
    simple_goals: SimpleGoals
    session_expires: datetime

# ===== PROFILE COMPLETION HELPERS =====

def calculate_profile_completion(profile: dict, profile_type: str) -> float:
    """Calculate profile completion percentage based on filled fields"""
    if profile_type == "PATIENT":
        sections = ["basic_info", "physical_metrics", "activity_profile", "health_history", "dietary_profile", "goals_preferences"]
    elif profile_type == "PROVIDER":
        sections = ["professional_identity", "credentials", "practice_info", "preferences"]
    elif profile_type == "FAMILY":
        sections = ["family_structure", "family_members", "household_management", "care_coordination"]
    else:
        return 100.0  # Guest profiles are always complete
    
    completed_sections = sum(1 for section in sections if profile.get(section) is not None)
    return (completed_sections / len(sections)) * 100.0

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Health & Nutrition Platform API"}

# ===== PROFILE MANAGEMENT API ENDPOINTS =====

# Patient Profile Endpoints
@api_router.post("/profiles/patient", response_model=PatientProfile)
async def create_patient_profile(profile: PatientProfileCreate):
    profile_dict = profile.dict()
    profile_obj = PatientProfile(**profile_dict)
    profile_obj.profile_completion = calculate_profile_completion(profile_dict, "PATIENT")
    
    # Check if profile already exists
    existing = await db.patient_profiles.find_one({"user_id": profile.user_id})
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")
    
    await db.patient_profiles.insert_one(profile_obj.dict())
    return profile_obj

@api_router.get("/profiles/patient/{user_id}", response_model=PatientProfile)
async def get_patient_profile(user_id: str):
    profile = await db.patient_profiles.find_one({"user_id": user_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return PatientProfile(**profile)

@api_router.put("/profiles/patient/{user_id}", response_model=PatientProfile)
async def update_patient_profile(user_id: str, update: PatientProfileUpdate):
    existing = await db.patient_profiles.find_one({"user_id": user_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_dict = {k: v for k, v in update.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    # Merge existing profile with updates
    merged_profile = {**existing, **update_dict}
    merged_profile["profile_completion"] = calculate_profile_completion(merged_profile, "PATIENT")
    
    await db.patient_profiles.update_one(
        {"user_id": user_id},
        {"$set": update_dict}
    )
    
    updated_profile = await db.patient_profiles.find_one({"user_id": user_id})
    return PatientProfile(**updated_profile)

@api_router.delete("/profiles/patient/{user_id}")
async def delete_patient_profile(user_id: str):
    result = await db.patient_profiles.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}

# Provider Profile Endpoints
@api_router.post("/profiles/provider", response_model=ProviderProfile)
async def create_provider_profile(profile: ProviderProfileCreate):
    profile_dict = profile.dict()
    profile_obj = ProviderProfile(**profile_dict)
    profile_obj.profile_completion = calculate_profile_completion(profile_dict, "PROVIDER")
    
    existing = await db.provider_profiles.find_one({"user_id": profile.user_id})
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")
    
    await db.provider_profiles.insert_one(profile_obj.dict())
    return profile_obj

@api_router.get("/profiles/provider/{user_id}", response_model=ProviderProfile)
async def get_provider_profile(user_id: str):
    profile = await db.provider_profiles.find_one({"user_id": user_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProviderProfile(**profile)

@api_router.put("/profiles/provider/{user_id}", response_model=ProviderProfile)
async def update_provider_profile(user_id: str, update: ProviderProfileUpdate):
    existing = await db.provider_profiles.find_one({"user_id": user_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_dict = {k: v for k, v in update.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    merged_profile = {**existing, **update_dict}
    merged_profile["profile_completion"] = calculate_profile_completion(merged_profile, "PROVIDER")
    
    await db.provider_profiles.update_one(
        {"user_id": user_id},
        {"$set": update_dict}
    )
    
    updated_profile = await db.provider_profiles.find_one({"user_id": user_id})
    return ProviderProfile(**updated_profile)

@api_router.delete("/profiles/provider/{user_id}")
async def delete_provider_profile(user_id: str):
    result = await db.provider_profiles.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}

# Family Profile Endpoints
@api_router.post("/profiles/family", response_model=FamilyProfile)
async def create_family_profile(profile: FamilyProfileCreate):
    profile_dict = profile.dict()
    profile_obj = FamilyProfile(**profile_dict)
    profile_obj.profile_completion = calculate_profile_completion(profile_dict, "FAMILY")
    
    existing = await db.family_profiles.find_one({"user_id": profile.user_id})
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")
    
    await db.family_profiles.insert_one(profile_obj.dict())
    return profile_obj

@api_router.get("/profiles/family/{user_id}", response_model=FamilyProfile)
async def get_family_profile(user_id: str):
    profile = await db.family_profiles.find_one({"user_id": user_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return FamilyProfile(**profile)

@api_router.put("/profiles/family/{user_id}", response_model=FamilyProfile)
async def update_family_profile(user_id: str, update: FamilyProfileUpdate):
    existing = await db.family_profiles.find_one({"user_id": user_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_dict = {k: v for k, v in update.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    merged_profile = {**existing, **update_dict}
    merged_profile["profile_completion"] = calculate_profile_completion(merged_profile, "FAMILY")
    
    await db.family_profiles.update_one(
        {"user_id": user_id},
        {"$set": update_dict}
    )
    
    updated_profile = await db.family_profiles.find_one({"user_id": user_id})
    return FamilyProfile(**updated_profile)

@api_router.delete("/profiles/family/{user_id}")
async def delete_family_profile(user_id: str):
    result = await db.family_profiles.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}

# Guest Profile Endpoints
@api_router.post("/profiles/guest", response_model=GuestProfile)
async def create_guest_profile(profile: GuestProfileCreate):
    profile_dict = profile.dict()
    profile_obj = GuestProfile(**profile_dict)
    
    # Clean up expired guest profiles periodically
    await db.guest_profiles.delete_many({"session_expires": {"$lt": datetime.utcnow()}})
    
    await db.guest_profiles.insert_one(profile_obj.dict())
    return profile_obj

@api_router.get("/profiles/guest/{session_id}", response_model=GuestProfile)
async def get_guest_profile(session_id: str):
    profile = await db.guest_profiles.find_one({
        "session_id": session_id,
        "session_expires": {"$gt": datetime.utcnow()}
    })
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found or expired")
    return GuestProfile(**profile)

@api_router.delete("/profiles/guest/{session_id}")
async def delete_guest_profile(session_id: str):
    result = await db.guest_profiles.delete_one({"session_id": session_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}

# Profile Completion Status Endpoints
@api_router.get("/profiles/completion/{user_id}")
async def get_profile_completion_status(user_id: str, role: str):
    if role.upper() == "PATIENT":
        profile = await db.patient_profiles.find_one({"user_id": user_id})
    elif role.upper() == "PROVIDER":
        profile = await db.provider_profiles.find_one({"user_id": user_id})
    elif role.upper() == "FAMILY":
        profile = await db.family_profiles.find_one({"user_id": user_id})
    else:
        raise HTTPException(status_code=400, detail="Invalid role specified")
    
    if not profile:
        return {"completion_percentage": 0.0, "missing_sections": []}
    
    completion = profile.get("profile_completion", 0.0)
    
    # Determine missing sections
    missing_sections = []
    if role.upper() == "PATIENT":
        sections = ["basic_info", "physical_metrics", "activity_profile", "health_history", "dietary_profile", "goals_preferences"]
    elif role.upper() == "PROVIDER":
        sections = ["professional_identity", "credentials", "practice_info", "preferences"]
    else:  # FAMILY
        sections = ["family_structure", "family_members", "household_management", "care_coordination"]
    
    missing_sections = [section for section in sections if not profile.get(section)]
    
    return {
        "completion_percentage": completion,
        "missing_sections": missing_sections,
        "total_sections": len(sections),
        "completed_sections": len(sections) - len(missing_sections)
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Role-specific API endpoints
@api_router.post("/users", response_model=UserProfile)
async def create_user(user: UserProfileCreate):
    user_dict = user.dict()
    user_obj = UserProfile(**user_dict)
    _ = await db.users.insert_one(user_obj.dict())
    return user_obj

@api_router.get("/users/{role}", response_model=List[UserProfile])
async def get_users_by_role(role: str):
    users = await db.users.find({"role": role}).to_list(1000)
    return [UserProfile(**user) for user in users]

@api_router.post("/health-metrics", response_model=HealthMetric)
async def create_health_metric(metric: HealthMetricCreate):
    metric_dict = metric.dict()
    metric_obj = HealthMetric(**metric_dict)
    _ = await db.health_metrics.insert_one(metric_obj.dict())
    return metric_obj

@api_router.get("/health-metrics/{user_id}", response_model=List[HealthMetric])
async def get_user_health_metrics(user_id: str):
    metrics = await db.health_metrics.find({"user_id": user_id}).to_list(1000)
    return [HealthMetric(**metric) for metric in metrics]

# Patient-specific endpoints
@api_router.get("/patient/dashboard/{user_id}")
async def get_patient_dashboard(user_id: str):
    return {
        "user_id": user_id,
        "welcome_message": "Welcome back, Sarah!",
        "nutrition_summary": {
            "calories": {"current": 1847, "remaining": 153, "target": 2000},
            "protein": {"current": 98, "target": 120, "unit": "g"},
            "carbs": {"current": 147, "target": 200, "unit": "g"},
            "fat": {"current": 52, "target": 65, "unit": "g"}
        },
        "health_metrics": {
            "blood_pressure": {"value": "120/80", "unit": "mmHg", "status": "Normal"},
            "weight": {"value": 68.5, "unit": "kg", "change": -0.3},
            "glucose": {"value": 95, "unit": "mg/dL", "status": "Normal"}
        },
        "goals": {
            "daily_steps": {"current": 8432, "target": 10000, "progress": 84},
            "water_intake": {"current": 6, "target": 8, "progress": 75},
            "weekly_exercise": {"current": 3, "target": 5, "progress": 60}
        },
        "recent_meals": [
            {"id": 1, "meal": "Breakfast", "food": "Oatmeal with berries", "calories": 350, "time": "8:00 AM"},
            {"id": 2, "meal": "Lunch", "food": "Grilled chicken salad", "calories": 425, "time": "12:30 PM"}
        ],
        "ai_recommendations": [
            {"type": "meal", "title": "Meal Suggestion", "message": "Try a protein-rich snack like Greek yogurt to reach your daily protein goal."},
            {"type": "hydration", "title": "Hydration Reminder", "message": "You're 2 glasses behind your water goal. Have a glass now!"},
            {"type": "activity", "title": "Activity Boost", "message": "A 15-minute walk would help you reach your step goal."}
        ]
    }

@api_router.get("/patient/food-log/{user_id}")
async def get_patient_food_log(user_id: str):
    return {
        "user_id": user_id,
        "today_entries": [
            {"id": 1, "time": "8:00 AM", "meal": "Breakfast", "food": "Oatmeal with berries", "calories": 350},
            {"id": 2, "time": "12:30 PM", "meal": "Lunch", "food": "Grilled chicken salad", "calories": 425}
        ],
        "total_calories": 775,
        "remaining_calories": 1225
    }

@api_router.get("/patient/health-metrics/{user_id}")
async def get_patient_health_metrics(user_id: str):
    return {
        "user_id": user_id,
        "metrics": [
            {"type": "weight", "value": 68.5, "unit": "kg", "date": "2024-01-15", "trend": "decreasing"},
            {"type": "blood_pressure", "systolic": 120, "diastolic": 80, "date": "2024-01-15", "status": "normal"},
            {"type": "glucose", "value": 95, "unit": "mg/dL", "date": "2024-01-15", "status": "normal"}
        ]
    }

# Provider-specific endpoints
@api_router.get("/provider/dashboard/{user_id}")
async def get_provider_dashboard(user_id: str):
    return {
        "user_id": user_id,
        "welcome_message": "Good morning, Dr. Smith!",
        "patient_overview": {
            "active_patients": 247,
            "prescriptions": 156,
            "compliance_rate": 94,
            "todays_visits": 12
        },
        "clinical_alerts": [
            {"id": 1, "patient": "John D.", "type": "critical", "message": "Blood pressure spike detected", "priority": "high"},
            {"id": 2, "patient": "Sarah M.", "type": "warning", "message": "Missed medication doses", "priority": "medium"},
            {"id": 3, "patient": "Mike R.", "type": "info", "message": "Excellent progress this week", "priority": "low"}
        ],
        "todays_appointments": [
            {"id": 1, "time": "9:00 AM", "patient": "Emma Wilson", "type": "Nutrition consultation", "status": "completed"},
            {"id": 2, "time": "11:30 AM", "patient": "David Chen", "type": "Follow-up appointment", "status": "in_progress"},
            {"id": 3, "time": "2:00 PM", "patient": "Lisa Garcia", "type": "Initial assessment", "status": "upcoming"}
        ],
        "patient_progress": {
            "weight_loss_goals": {"percentage": 87, "description": "patients on track"},
            "medication_adherence": {"percentage": 94, "description": "compliance rate"},
            "lifestyle_changes": {"percentage": 76, "description": "showing improvement"}
        }
    }

@api_router.get("/provider/patients")
async def get_provider_patients():
    return {
        "patients": [
            {"id": 1, "name": "John Doe", "age": 45, "condition": "Diabetes", "last_visit": "2024-01-10", "status": "stable"},
            {"id": 2, "name": "Sarah Miller", "age": 38, "condition": "Hypertension", "last_visit": "2024-01-12", "status": "improving"},
            {"id": 3, "name": "Mike Rodriguez", "age": 52, "condition": "Obesity", "last_visit": "2024-01-08", "status": "excellent"}
        ],
        "total_patients": 247,
        "active_patients": 189
    }

@api_router.get("/provider/clinical-tools")
async def get_clinical_tools():
    return {
        "tools": [
            {"name": "Diet Prescription Generator", "description": "Create evidence-based diet plans", "category": "nutrition"},
            {"name": "Drug Interaction Checker", "description": "Check for medication interactions", "category": "pharmacy"},
            {"name": "BMI Calculator", "description": "Calculate and track BMI over time", "category": "assessment"},
            {"name": "Risk Assessment", "description": "Cardiovascular risk calculator", "category": "assessment"}
        ]
    }

# Family-specific endpoints
@api_router.get("/family/dashboard/{user_id}")
async def get_family_dashboard(user_id: str):
    return {
        "user_id": user_id,
        "family_overview": {
            "family_members": 4,
            "health_alerts": 2,
            "appointments": 3,
            "coverage": "100%"
        },
        "family_members": [
            {"id": 1, "name": "John (Dad)", "age": 42, "status": "healthy", "avatar_color": "blue"},
            {"id": 2, "name": "Sarah (Mom)", "age": 38, "status": "healthy", "avatar_color": "pink"},
            {"id": 3, "name": "Emma (12)", "age": 12, "status": "checkup_due", "avatar_color": "purple"},
            {"id": 4, "name": "Alex (8)", "age": 8, "status": "healthy", "avatar_color": "green"}
        ],
        "meal_planning": {
            "week_completion": 85,
            "planned_days": 5,
            "total_days": 7,
            "next_meals": [
                {"day": "Tonight", "meal": "Grilled Chicken", "status": "ready"},
                {"day": "Tomorrow", "meal": "Pasta Primavera", "status": "planned"}
            ]
        },
        "health_alerts": [
            {"type": "checkup", "member": "Emma", "message": "Due in 2 weeks", "priority": "medium"},
            {"type": "vaccination", "member": "All", "message": "All up to date", "priority": "low"}
        ],
        "upcoming_appointments": [
            {"date": "Tomorrow", "time": "3:00 PM", "member": "Emma", "type": "Dental Checkup"},
            {"date": "Wednesday", "time": "4:30 PM", "member": "Alex", "type": "Soccer Practice"},
            {"date": "Friday", "time": "6:00 PM", "member": "Family", "type": "Dinner Planning"}
        ]
    }

@api_router.get("/family/meal-planning/{user_id}")
async def get_family_meal_planning(user_id: str):
    return {
        "user_id": user_id,
        "weekly_plan": {
            "monday": {"breakfast": "Pancakes", "lunch": "Sandwiches", "dinner": "Chicken Stir-fry"},
            "tuesday": {"breakfast": "Oatmeal", "lunch": "Soup", "dinner": "Pasta"},
            "wednesday": {"breakfast": "Toast", "lunch": "Salad", "dinner": "Fish"},
            "thursday": {"breakfast": "Cereal", "lunch": "Leftovers", "dinner": "Pizza"},
            "friday": {"breakfast": "Eggs", "lunch": "Wraps", "dinner": "Tacos"}
        },
        "shopping_list": ["Chicken breast", "Vegetables", "Pasta", "Fish fillets", "Eggs", "Bread"],
        "family_recipes": [
            {"id": 1, "name": "Mom's Healthy Lasagna", "rating": 5, "category": "dinner", "kid_approved": True},
            {"id": 2, "name": "Rainbow Smoothie Bowls", "rating": 4, "category": "breakfast", "kid_approved": True}
        ]
    }

# Guest-specific endpoints
@api_router.get("/guest/dashboard")
async def get_guest_dashboard():
    return {
        "session_info": {
            "quick_logs": 5,
            "session_time": "15m",
            "features_used": 3,
            "experience": "Good"
        },
        "todays_entries": [
            {"id": 1, "name": "Coffee with milk", "time": "8:00 AM", "calories": 50},
            {"id": 2, "name": "Toast with avocado", "time": "8:30 AM", "calories": 320}
        ],
        "nutrition_summary": {
            "total_calories": 370,
            "meals_logged": {"breakfast": 370, "lunch": 0, "dinner": 0}
        },
        "simple_goals": [
            {"name": "Eat 5 servings of fruits/vegetables", "current": 2, "target": 5, "progress": 40},
            {"name": "Drink 8 glasses of water", "current": 3, "target": 8, "progress": 37.5},
            {"name": "Log all meals today", "current": 1, "target": 3, "progress": 33.3}
        ],
        "nutrition_tips": {
            "daily_tip": {
                "title": "Stay Hydrated",
                "content": "Drinking water before meals can help with portion control and digestion. Aim for at least 8 glasses throughout the day."
            },
            "quick_facts": [
                {"title": "🥗 Fiber Fact", "content": "Adults need 25-35g of fiber daily for optimal digestive health."},
                {"title": "💪 Protein Power", "content": "Include protein in every meal to help maintain stable blood sugar levels."},
                {"title": "🌈 Color Variety", "content": "Eating different colored fruits and vegetables ensures diverse nutrients."}
            ]
        },
        "message": "Guest session active - data will not be permanently saved"
    }

@api_router.post("/guest/quick-log")
async def create_guest_food_log(food_data: dict):
    return {
        "success": True,
        "message": "Food logged successfully (session only)",
        "entry": {
            "id": f"guest_{datetime.now().strftime('%H%M%S')}",
            "food": food_data.get("food_name", "Unknown food"),
            "calories": food_data.get("calories", 0),
            "time": datetime.now().strftime("%I:%M %p")
        }
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
