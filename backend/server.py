from fastapi import FastAPI, APIRouter, HTTPException, Body
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

# Import AI services
from ai_services import get_nutrition_insights, get_smart_food_suggestions, get_health_correlations, get_clinical_insights


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
    update_dict["profile_completion"] = merged_profile["profile_completion"]
    
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
    update_dict["profile_completion"] = merged_profile["profile_completion"]
    
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
    update_dict["profile_completion"] = merged_profile["profile_completion"]
    
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

# ===== PHASE 1: ADVANCED ROLE-SPECIFIC API ENDPOINTS =====

# ===== PATIENT ANALYTICS & INSIGHTS =====

class NutritionTrend(BaseModel):
    date: str
    calories: int
    protein: float
    carbs: float
    fat: float

class HealthInsight(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    insight_type: str  # correlation, recommendation, pattern, alert
    title: str
    message: str
    confidence: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FoodLogEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    food_name: str
    quantity: float
    unit: str
    calories: int
    meal_type: str  # breakfast, lunch, dinner, snack
    logged_at: datetime = Field(default_factory=datetime.utcnow)
    photo_url: Optional[str] = None

class SymptomEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    symptom_type: str  # energy, mood, digestion, sleep
    severity: int  # 1-10 scale
    notes: Optional[str] = None
    recorded_at: datetime = Field(default_factory=datetime.utcnow)

# ===== PROVIDER CLINICAL TOOLS =====

class PatientAssignment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider_id: str
    patient_id: str
    assignment_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "active"  # active, inactive, completed

class TreatmentPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider_id: str
    patient_id: str
    plan_type: str  # nutrition, medication, lifestyle
    recommendations: List[Dict[str, Any]]
    target_outcomes: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ClinicalNote(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider_id: str
    patient_id: str
    note_type: str  # consultation, assessment, progress
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ===== FAMILY COORDINATION =====

class FamilyGoal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    family_id: str
    goal_type: str  # nutrition, fitness, health
    title: str
    description: str
    target_value: Optional[float] = None
    current_progress: float = 0.0
    participants: List[str] = []  # family member IDs
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    status: str = "active"  # active, completed, paused

class MealPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    family_id: str
    week_start: datetime
    meals: Dict[str, Dict[str, str]]  # day -> meal_type -> recipe_name
    shopping_list: List[str] = []
    dietary_restrictions: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ===== GUEST SESSION MANAGEMENT =====

class GuestSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    activity_log: List[Dict[str, Any]] = []
    preferences: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime

# ===== ADVANCED API ENDPOINTS =====

# Patient Analytics Endpoints
@api_router.get("/patient/analytics/{user_id}")
async def get_patient_analytics(user_id: str):
    """Get comprehensive analytics for patient with AI-powered insights"""
    
    # Sample user data - in real app, this would come from database
    user_data = {
        "user_id": user_id,
        "age": 32,
        "gender": "female",
        "activity_level": "moderately_active",
        "goals": ["weight_loss", "energy_improvement"],
        "diet_type": "mediterranean",
        "avg_calories": 2030,
        "avg_protein": 92,
        "avg_carbs": 175,
        "avg_fat": 68,
        "weight": 68.5,
        "energy_level": 7.2,
        "sleep_quality": 7.5
    }
    
    # Generate AI-powered insights
    try:
        ai_insights = await get_nutrition_insights(user_data)
    except Exception as e:
        logger.error(f"AI insights error: {e}")
        ai_insights = {"insights": [], "recommendations": [], "confidence": 0.0}
    
    # Generate health correlations with AI
    health_data = {
        "daily_logs": [{"date": "2024-01-15", "energy": 7.5, "protein": 95}],
        "sleep_patterns": "consistent_7h",
        "exercise_frequency": "3x_week",
        "energy_trend": "improving",
        "weight_trend": "decreasing",
        "mood_patterns": "stable_positive"
    }
    
    try:
        ai_correlations = await get_health_correlations(health_data)
    except Exception as e:
        logger.error(f"AI correlations error: {e}")
        ai_correlations = {"correlations": []}
    
    return {
        "user_id": user_id,
        "nutrition_trends": [
            {"date": "2024-01-15", "calories": 2100, "protein": 95, "carbs": 180, "fat": 70},
            {"date": "2024-01-14", "calories": 1950, "protein": 88, "carbs": 165, "fat": 65},
            {"date": "2024-01-13", "calories": 2200, "protein": 102, "carbs": 195, "fat": 75},
            {"date": "2024-01-12", "calories": 1850, "protein": 85, "carbs": 155, "fat": 62},
            {"date": "2024-01-11", "calories": 2050, "protein": 92, "carbs": 175, "fat": 68}
        ],
        "health_correlations": ai_correlations.get("correlations", [
            {"metric": "energy_level", "correlation_with": "protein_intake", "strength": 0.75, "insight": "Higher protein intake correlates with better energy levels"},
            {"metric": "sleep_quality", "correlation_with": "caffeine_intake", "strength": -0.65, "insight": "Reduced caffeine after 2 PM improves sleep quality"},
            {"metric": "mood", "correlation_with": "exercise", "strength": 0.82, "insight": "Regular exercise significantly improves mood scores"}
        ]),
        "goal_progress": {
            "weight_loss": {"target": 70, "current": 68.5, "progress": 85, "trend": "on_track"},
            "fitness": {"target": 5, "current": 3, "progress": 60, "trend": "needs_improvement"},
            "nutrition": {"target": 100, "current": 78, "progress": 78, "trend": "good"}
        },
        "ai_powered_insights": {
            "source": ai_insights.get("source", "default"),
            "confidence": ai_insights.get("confidence", 0.6),
            "insights": ai_insights.get("insights", ["Analysis completed with available data"]),
            "recommendations": ai_insights.get("recommendations", ["Continue current healthy practices"]),
            "action_items": ai_insights.get("action_items", ["Monitor progress regularly"])
        },
        "personal_insights": ai_insights.get("insights", [
            {"type": "achievement", "message": "You've maintained your target calorie range for 5 consecutive days!", "date": "2024-01-15"},
            {"type": "recommendation", "message": "Consider adding more fiber-rich vegetables to your lunch meals", "date": "2024-01-15"},
            {"type": "pattern", "message": "Your energy levels are highest on days when you exercise in the morning", "date": "2024-01-14"}
        ]),
        "energy_patterns": {
            "morning": {"average": 7.2, "trend": "stable"},
            "afternoon": {"average": 6.8, "trend": "declining"},
            "evening": {"average": 6.5, "trend": "stable"}
        },
        "weekly_summary": {
            "average_calories": 2030,
            "protein_goal_met": 6,
            "exercise_sessions": 3,
            "weight_change": -0.3,
            "mood_score": 7.8,
            "sleep_quality": 7.5
        }
    }

@api_router.get("/patient/smart-suggestions/{user_id}")
async def get_smart_food_suggestions(user_id: str):
    """Get AI-powered food suggestions based on eating patterns"""
    
    # Sample user profile - in real app, this would come from database
    user_profile = {
        "diet_type": "mediterranean",
        "allergies": ["tree_nuts"],
        "favorite_foods": ["salmon", "quinoa", "berries", "greek_yogurt"],
        "cooking_time": 30
    }
    
    current_intake = {
        "calories": 1200,
        "protein": 45,
        "calories_remaining": 800,
        "time_of_day": "afternoon"
    }
    
    # Get AI-powered food suggestions
    try:
        ai_suggestions = await get_smart_food_suggestions(user_profile, current_intake)
    except Exception as e:
        logger.error(f"AI food suggestions error: {e}")
        ai_suggestions = []
    
    # Default suggestions if AI fails
    default_suggestions = [
        {"name": "Greek Yogurt with Berries", "calories": 150, "reason": "Your usual morning snack", "frequency": "often"},
        {"name": "Grilled Chicken Salad", "calories": 350, "reason": "Perfect for your lunch protein goal", "frequency": "weekly"},
        {"name": "Almonds (1 oz)", "calories": 164, "reason": "Healthy fat you enjoyed yesterday", "frequency": "daily"},
        {"name": "Green Smoothie", "calories": 180, "reason": "Boosts your vegetable intake", "frequency": "sometimes"}
    ]
    
    return {
        "user_id": user_id,
        "ai_powered": len(ai_suggestions) > 0,
        "quick_add_suggestions": ai_suggestions if ai_suggestions else default_suggestions,
        "meal_pattern_insights": {
            "breakfast_time": "8:15 AM",
            "lunch_time": "12:30 PM",
            "dinner_time": "7:00 PM",
            "snack_preferences": ["nuts", "fruits", "yogurt"],
            "favorite_cuisines": ["Mediterranean", "Asian", "Mexican"]
        },
        "nutrition_gaps": [
            {"nutrient": "Fiber", "current": 18, "target": 25, "suggestion": "Add beans or lentils to lunch"},
            {"nutrient": "Omega-3", "current": "low", "target": "adequate", "suggestion": "Include fatty fish twice weekly"},
            {"nutrient": "Vitamin D", "current": "insufficient", "target": "adequate", "suggestion": "Consider fortified foods or supplements"}
        ]
    }

@api_router.post("/patient/food-log")
async def log_food(food_entry: dict):
    """Smart food logging with automatic nutrition lookup and AI pattern recognition"""
    
    # Get AI-powered food analysis
    food_name = food_entry.get("food_name", "Unknown Food")
    try:
        # Simulate AI nutrition analysis
        ai_analysis = await analyze_food_with_ai(food_name, food_entry)
    except Exception as e:
        logger.error(f"AI food analysis error: {e}")
        ai_analysis = None
    
    # Enhanced nutrition lookup with AI suggestions
    enhanced_entry = {
        "id": str(uuid.uuid4()),
        "food_name": food_name,
        "calories": food_entry.get("calories") or (ai_analysis.get("calories") if ai_analysis else 200),
        "protein": food_entry.get("protein") or (ai_analysis.get("protein") if ai_analysis else 15),
        "carbs": food_entry.get("carbs") or (ai_analysis.get("carbs") if ai_analysis else 25),
        "fat": food_entry.get("fat") or (ai_analysis.get("fat") if ai_analysis else 8),
        "fiber": ai_analysis.get("fiber") if ai_analysis else 3,
        "sugar": ai_analysis.get("sugar") if ai_analysis else 5,
        "confidence": ai_analysis.get("confidence") if ai_analysis else 0.80,
        "similar_foods": ai_analysis.get("similar_foods") if ai_analysis else ["Chicken Breast", "Turkey Breast", "Lean Beef"],
        "logged_at": datetime.utcnow().isoformat(),
        "meal_type": food_entry.get("meal_type") or get_current_meal_type(),
        "ai_enhanced": bool(ai_analysis)
    }
    
    # AI-powered insights based on recent eating patterns
    ai_insights = []
    if ai_analysis:
        ai_insights.extend(ai_analysis.get("insights", []))
    
    # Pattern recognition insights
    pattern_insights = analyze_eating_patterns(enhanced_entry)
    ai_insights.extend(pattern_insights)
    
    return {
        "success": True,
        "food_entry": enhanced_entry,
        "daily_totals": {
            "calories": 1450 + enhanced_entry["calories"],
            "protein": 78 + enhanced_entry["protein"],
            "carbs": 145 + enhanced_entry["carbs"],
            "fat": 52 + enhanced_entry["fat"],
            "fiber": 18 + enhanced_entry["fiber"]
        },
        "ai_insights": ai_insights,
        "pattern_recognition": {
            "meal_timing_pattern": "Consistent with your usual lunch time",
            "nutrition_balance": "Good protein choice for post-workout meal",
            "frequency_insight": "You've had similar foods 3 times this week",
            "suggestions": [
                "Great protein choice! This helps meet your daily protein goal.",
                "Consider adding some vegetables for extra fiber and nutrients.",
                "This meal fits well with your Mediterranean diet pattern."
            ]
        },
        "smart_suggestions": {
            "complementary_foods": [
                {"name": "Mixed Green Salad", "reason": "Adds fiber and micronutrients"},
                {"name": "Avocado Slices", "reason": "Healthy fats to balance the meal"},
                {"name": "Greek Yogurt", "reason": "Additional protein and probiotics"}
            ],
            "portion_feedback": generate_portion_feedback(enhanced_entry),
            "timing_feedback": f"Good timing for {enhanced_entry['meal_type'].lower()}"
        }
    }

async def analyze_food_with_ai(food_name: str, food_entry: dict) -> dict:
    """Analyze food with AI for enhanced nutrition data"""
    # This would integrate with the AI service
    try:
        # Simulate AI food analysis
        ai_analysis = {
            "calories": estimate_calories_from_name(food_name),
            "protein": estimate_protein_from_name(food_name),
            "carbs": estimate_carbs_from_name(food_name), 
            "fat": estimate_fat_from_name(food_name),
            "fiber": estimate_fiber_from_name(food_name),
            "sugar": estimate_sugar_from_name(food_name),
            "confidence": 0.85,
            "similar_foods": get_similar_foods(food_name),
            "insights": [
                f"Nutritional analysis of {food_name} completed",
                "Values estimated using AI food recognition"
            ]
        }
        return ai_analysis
    except Exception as e:
        logger.error(f"AI food analysis failed: {e}")
        return None

def analyze_eating_patterns(food_entry: dict) -> list:
    """Analyze eating patterns for insights"""
    insights = []
    
    # Time-based insights
    current_hour = datetime.utcnow().hour
    if current_hour < 10:
        insights.append("Great start to the day with a nutritious breakfast!")
    elif current_hour < 15:
        insights.append("Perfect lunch timing for sustained energy.")
    elif current_hour < 20:
        insights.append("Good dinner choice for evening nutrition.")
    else:
        insights.append("Late meal - consider earlier dinner for better sleep.")
    
    # Nutrition-based insights
    if food_entry["protein"] > 20:
        insights.append("Excellent protein content - great for muscle maintenance.")
    if food_entry["fiber"] > 5:
        insights.append("High fiber content supports digestive health.")
    
    return insights

def get_current_meal_type() -> str:
    """Determine current meal type based on time"""
    current_hour = datetime.utcnow().hour
    if current_hour < 11:
        return "Breakfast"
    elif current_hour < 16:
        return "Lunch"
    elif current_hour < 20:
        return "Dinner"
    else:
        return "Snack"

def estimate_calories_from_name(food_name: str) -> int:
    """Estimate calories based on food name"""
    food_lower = food_name.lower()
    if any(word in food_lower for word in ["salad", "vegetables", "lettuce"]):
        return 50 + (len(food_name) * 2)
    elif any(word in food_lower for word in ["chicken", "fish", "meat"]):
        return 200 + (len(food_name) * 3)
    elif any(word in food_lower for word in ["pasta", "rice", "bread"]):
        return 150 + (len(food_name) * 4)
    else:
        return 150

def estimate_protein_from_name(food_name: str) -> int:
    """Estimate protein based on food name"""
    food_lower = food_name.lower()
    if any(word in food_lower for word in ["chicken", "fish", "meat", "protein"]):
        return 25 + (len(food_name) // 2)
    elif any(word in food_lower for word in ["yogurt", "cheese", "milk"]):
        return 12 + (len(food_name) // 3)
    else:
        return 5 + (len(food_name) // 4)

def estimate_carbs_from_name(food_name: str) -> int:
    """Estimate carbs based on food name"""
    food_lower = food_name.lower()
    if any(word in food_lower for word in ["pasta", "rice", "bread", "potato"]):
        return 35 + (len(food_name) // 2)
    elif any(word in food_lower for word in ["fruit", "apple", "banana"]):
        return 20 + (len(food_name) // 3)
    else:
        return 10 + (len(food_name) // 4)

def estimate_fat_from_name(food_name: str) -> int:
    """Estimate fat based on food name"""
    food_lower = food_name.lower()
    if any(word in food_lower for word in ["avocado", "nuts", "oil", "butter"]):
        return 15 + (len(food_name) // 3)
    elif any(word in food_lower for word in ["salmon", "cheese", "cream"]):
        return 12 + (len(food_name) // 4)
    else:
        return 5 + (len(food_name) // 5)

def estimate_fiber_from_name(food_name: str) -> int:
    """Estimate fiber based on food name"""
    food_lower = food_name.lower()
    if any(word in food_lower for word in ["vegetables", "salad", "beans", "fiber"]):
        return 8 + (len(food_name) // 4)
    elif any(word in food_lower for word in ["fruit", "apple", "pear"]):
        return 4 + (len(food_name) // 5)
    else:
        return 2

def estimate_sugar_from_name(food_name: str) -> int:
    """Estimate sugar based on food name"""
    food_lower = food_name.lower()
    if any(word in food_lower for word in ["fruit", "sweet", "dessert", "cake"]):
        return 15 + (len(food_name) // 3)
    elif any(word in food_lower for word in ["yogurt", "milk"]):
        return 8 + (len(food_name) // 4)
    else:
        return 3

def get_similar_foods(food_name: str) -> list:
    """Get similar foods based on food name"""
    food_lower = food_name.lower()
    if any(word in food_lower for word in ["chicken", "poultry"]):
        return ["Turkey Breast", "Lean Beef", "Fish Fillet", "Tofu"]
    elif any(word in food_lower for word in ["salad", "vegetables"]):
        return ["Mixed Greens", "Spinach Salad", "Kale Salad", "Arugula"]
    elif any(word in food_lower for word in ["yogurt"]):
        return ["Greek Yogurt", "Low-fat Yogurt", "Protein Yogurt", "Dairy Alternative"]
    else:
        return ["Similar Food Option 1", "Similar Food Option 2", "Alternative Choice"]

def generate_portion_feedback(food_entry: dict) -> str:
    """Generate feedback about portion size"""
    calories = food_entry.get("calories", 0)
    if calories < 100:
        return "Small portion - consider if this meets your energy needs"
    elif calories < 300:
        return "Moderate portion size - good for a snack or light meal"
    elif calories < 600:
        return "Good portion size for a main meal"
    else:
        return "Large portion - consider splitting if trying to manage calories"

@api_router.get("/patient/symptoms-correlation/{user_id}")
async def get_symptoms_correlation(user_id: str):
    """Get correlations between diet and symptoms"""
    return {
        "user_id": user_id,
        "correlations": [
            {
                "symptom": "Energy Level",
                "strong_positive": ["protein_intake", "complex_carbs", "B_vitamins"],
                "strong_negative": ["processed_sugar", "alcohol", "excessive_caffeine"],
                "insights": ["Energy levels are 40% higher on days with adequate protein (>80g)"]
            },
            {
                "symptom": "Digestive Health",
                "strong_positive": ["fiber_intake", "probiotics", "water_intake"],
                "strong_negative": ["processed_foods", "excessive_dairy", "artificial_sweeteners"],
                "insights": ["Digestive scores improve by 60% with 25g+ fiber daily"]
            },
            {
                "symptom": "Sleep Quality",
                "strong_positive": ["magnesium", "tryptophan", "regular_meals"],
                "strong_negative": ["late_caffeine", "large_evening_meals", "alcohol"],
                "insights": ["Sleep quality is 35% better when avoiding caffeine after 2 PM"]
            }
        ],
        "recommendations": [
            "Track your energy levels for 2 weeks to identify patterns",
            "Consider keeping a mood-food diary",
            "Monitor sleep quality in relation to evening meal timing"
        ]
    }

# Patient Medication Reminder Endpoints
@api_router.get("/patient/medications/{user_id}")
async def get_patient_medications(user_id: str):
    """Get patient's medication reminders and schedule"""
    return {
        "user_id": user_id,
        "medications": [
            {
                "id": "med_001",
                "name": "Metformin",
                "dosage": "500mg",
                "frequency": "twice_daily",
                "times": ["08:00", "20:00"],
                "with_food": True,
                "condition": "Type 2 Diabetes",
                "prescriber": "Dr. Smith",
                "start_date": "2024-01-01",
                "end_date": "2024-06-01",
                "adherence_rate": 95,
                "last_taken": "2024-01-15 20:00",
                "next_due": "2024-01-16 08:00",
                "status": "active"
            },
            {
                "id": "med_002", 
                "name": "Omega-3 Supplement",
                "dosage": "1000mg",
                "frequency": "daily",
                "times": ["08:00"],
                "with_food": True,
                "condition": "Heart Health",
                "prescriber": "Self-prescribed",
                "start_date": "2024-01-01",
                "end_date": None,
                "adherence_rate": 87,
                "last_taken": "2024-01-15 08:15",
                "next_due": "2024-01-16 08:00",
                "status": "active"
            }
        ],
        "reminders": [
            {
                "id": "rem_001",
                "medication_id": "med_001",
                "time": "08:00",
                "status": "completed",
                "completed_at": "2024-01-16 08:05"
            },
            {
                "id": "rem_002",
                "medication_id": "med_002",
                "time": "08:00", 
                "status": "pending",
                "due_in_minutes": 45
            }
        ],
        "adherence_stats": {
            "overall_adherence": 91,
            "weekly_adherence": 95,
            "missed_doses_week": 1,
            "streak_days": 12
        },
        "ai_insights": [
            "Your adherence rate is excellent! Keep up the good work.",
            "Taking medications with food helps with absorption and reduces side effects.",
            "Consider setting phone reminders for the evening dose of Metformin."
        ]
    }

@api_router.post("/patient/medications/{user_id}/take")
async def mark_medication_taken(user_id: str, medication_data: dict):
    """Mark a medication as taken"""
    return {
        "success": True,
        "medication_id": medication_data.get("medication_id"),
        "taken_at": datetime.utcnow().isoformat(),
        "next_reminder": "2024-01-16 20:00",
        "streak_updated": True,
        "new_streak": 13
    }

@api_router.post("/patient/medications/{user_id}")
async def add_medication(user_id: str, medication: dict):
    """Add new medication to patient's list"""
    new_med = {
        "id": f"med_{uuid.uuid4()}",
        "name": medication.get("name"),
        "dosage": medication.get("dosage"),
        "frequency": medication.get("frequency"),
        "times": medication.get("times", []),
        "with_food": medication.get("with_food", False),
        "condition": medication.get("condition", ""),
        "prescriber": medication.get("prescriber", ""),
        "start_date": medication.get("start_date"),
        "end_date": medication.get("end_date"),
        "status": "active",
        "adherence_rate": 0
    }
    
    return {
        "success": True,
        "medication": new_med,
        "message": "Medication added successfully"
    }

# Patient Health Timeline Endpoints
@api_router.get("/patient/timeline/{user_id}")
async def get_health_timeline(user_id: str):
    """Get comprehensive health timeline with AI insights"""
    return {
        "user_id": user_id,
        "timeline_events": [
            {
                "id": "evt_001",
                "date": "2024-01-15",
                "type": "weight_measurement",
                "title": "Weight Check",
                "value": "68.5 kg",
                "category": "metrics",
                "details": "Lost 0.3kg from last week",
                "impact": "positive",
                "ai_note": "Consistent progress toward weight goal"
            },
            {
                "id": "evt_002",
                "date": "2024-01-14",
                "type": "exercise",
                "title": "Cardio Workout",
                "value": "45 minutes",
                "category": "activity",
                "details": "Running + strength training",
                "impact": "positive",
                "ai_note": "Excellent workout intensity for heart health"
            },
            {
                "id": "evt_003",
                "date": "2024-01-13",
                "type": "meal_log",
                "title": "High Protein Day",
                "value": "105g protein",
                "category": "nutrition",
                "details": "Exceeded daily protein goal by 15g",
                "impact": "positive",
                "ai_note": "Perfect protein intake for muscle maintenance"
            },
            {
                "id": "evt_004",
                "date": "2024-01-12",
                "type": "symptom",
                "title": "Low Energy",
                "value": "4/10 energy",
                "category": "symptoms",
                "details": "Felt tired throughout afternoon",
                "impact": "negative",
                "ai_note": "May be related to insufficient sleep (5.5 hours)"
            },
            {
                "id": "evt_005",
                "date": "2024-01-11",
                "type": "medication",
                "title": "Missed Evening Dose",
                "value": "Metformin 500mg",
                "category": "medication",
                "details": "Forgot to take evening medication",
                "impact": "negative",
                "ai_note": "Set consistent reminders to improve adherence"
            },
            {
                "id": "evt_006",
                "date": "2024-01-10",
                "type": "achievement",
                "title": "Weekly Goal Met",
                "value": "3/3 workouts completed",
                "category": "goals",
                "details": "Successfully completed weekly exercise goal",
                "impact": "positive",
                "ai_note": "Consistent exercise is improving overall health metrics"
            }
        ],
        "patterns": {
            "energy_correlation": {
                "pattern": "Energy levels higher on exercise days",
                "confidence": 0.82,
                "recommendation": "Maintain regular exercise schedule"
            },
            "sleep_impact": {
                "pattern": "Sleep <6 hours leads to poor energy next day",
                "confidence": 0.91,
                "recommendation": "Aim for 7-8 hours of sleep nightly"
            },
            "nutrition_consistency": {
                "pattern": "Protein goals met 5/7 days this week",
                "confidence": 0.95,
                "recommendation": "Plan protein sources in advance"
            }
        },
        "milestones": [
            {
                "date": "2024-01-15",
                "type": "weight_goal",
                "title": "Lost 2kg in 6 weeks",
                "description": "Reached intermediate weight loss milestone",
                "celebration": "Great progress! You're 40% toward your target."
            },
            {
                "date": "2024-01-10",
                "type": "consistency",
                "title": "30-day Exercise Streak",
                "description": "Completed 30 consecutive days with some form of exercise",
                "celebration": "Amazing dedication to your fitness journey!"
            }
        ],
        "ai_insights": [
            "Your energy levels correlate strongly with sleep duration - prioritize 7+ hours",
            "Exercise days show 30% better mood scores than sedentary days",
            "Medication adherence improved 15% since starting reminders"
        ],
        "categories_summary": {
            "metrics": {"total": 15, "positive_trend": 12},
            "activity": {"total": 23, "weekly_average": 5.2},
            "nutrition": {"total": 45, "goals_met": 38},
            "symptoms": {"total": 8, "resolved": 6},
            "medication": {"total": 12, "adherence_rate": 91},
            "goals": {"total": 6, "achieved": 4}
        }
    }

@api_router.post("/patient/timeline/{user_id}/event")
async def add_timeline_event(user_id: str, event: dict):
    """Add new event to health timeline"""
    new_event = {
        "id": f"evt_{uuid.uuid4()}",
        "date": event.get("date", datetime.utcnow().date().isoformat()),
        "type": event.get("type"),
        "title": event.get("title"),
        "value": event.get("value"),
        "category": event.get("category"),
        "details": event.get("details", ""),
        "impact": event.get("impact", "neutral"),
        "ai_note": ""  # Would be generated by AI
    }
    
    return {
        "success": True,
        "event": new_event,
        "message": "Timeline event added successfully"
    }

# Provider Clinical Endpoints
@api_router.get("/provider/clinical-insights/{provider_id}")
async def get_clinical_insights(provider_id: str):
    """Get clinical decision support and insights with AI"""
    
    # Sample provider data
    provider_data = {
        "provider_id": provider_id,
        "total_patients": 247,
        "patient_conditions": ["diabetes", "hypertension", "obesity"],
        "recent_outcomes": [
            {"condition": "diabetes", "avg_hba1c_change": -1.2},
            {"condition": "hypertension", "avg_bp_reduction": 15}
        ]
    }
    
    # Get AI-powered clinical insights
    try:
        ai_clinical_insights = await get_clinical_insights(provider_data)
    except Exception as e:
        logger.error(f"AI clinical insights error: {e}")
        ai_clinical_insights = {"insights": [], "recommendations": []}
    
    return {
        "provider_id": provider_id,
        "ai_powered_analysis": {
            "enabled": True,
            "insights": ai_clinical_insights.get("insights", []),
            "evidence_based_recommendations": ai_clinical_insights.get("recommendations", []),
            "confidence": ai_clinical_insights.get("confidence", 0.8)
        },
        "population_health": {
            "total_patients": 247,
            "diabetes_patients": 45,
            "hypertension_patients": 78,
            "obesity_patients": 89,
            "metabolic_syndrome": 23
        },
        "treatment_outcomes": [
            {"condition": "Type 2 Diabetes", "improvement_rate": 73, "average_hba1c_reduction": 1.2},
            {"condition": "Hypertension", "improvement_rate": 68, "average_bp_reduction": "15/8"},
            {"condition": "Obesity", "improvement_rate": 55, "average_weight_loss": 8.5}
        ],
        "evidence_based_recommendations": ai_clinical_insights.get("recommendations", [
            {
                "condition": "Pre-diabetes",
                "intervention": "Mediterranean Diet + Exercise",
                "evidence_level": "A",
                "success_rate": 85,
                "reference": "Diabetes Care 2023"
            },
            {
                "condition": "Hypertension",
                "intervention": "DASH Diet + Sodium Reduction",
                "evidence_level": "A",
                "success_rate": 78,
                "reference": "NEJM 2023"
            }
        ]),
        "drug_nutrient_interactions": [
            {"medication": "Warfarin", "nutrient": "Vitamin K", "interaction": "Monitor intake consistency"},
            {"medication": "Metformin", "nutrient": "Vitamin B12", "interaction": "May require supplementation"},
            {"medication": "Statins", "nutrient": "CoQ10", "interaction": "Consider supplementation"}
        ],
        "clinical_alerts": [
            {"patient_id": "pat_123", "alert": "HbA1c trending upward", "priority": "high", "action": "Review diet adherence"},
            {"patient_id": "pat_456", "alert": "Blood pressure well controlled", "priority": "low", "action": "Continue current plan"}
        ]
    }

@api_router.get("/provider/patient-analytics/{provider_id}")
async def get_provider_patient_analytics(provider_id: str):
    """Get comprehensive analytics across all patients"""
    return {
        "provider_id": provider_id,
        "patient_demographics": {
            "age_distribution": {"18-30": 15, "31-45": 45, "46-60": 78, "60+": 109},
            "gender_distribution": {"male": 118, "female": 129},
            "condition_prevalence": {
                "diabetes": 18.2,
                "hypertension": 31.6,
                "obesity": 36.0,
                "dyslipidemia": 24.3
            }
        },
        "treatment_effectiveness": {
            "diet_plans": {"prescribed": 187, "adhering": 142, "success_rate": 76},
            "medication_compliance": {"prescribed": 156, "compliant": 147, "compliance_rate": 94},
            "lifestyle_interventions": {"recommended": 203, "following": 154, "success_rate": 76}
        },
        "outcome_trends": [
            {"month": "2024-01", "weight_loss_success": 67, "bp_control": 78, "glucose_control": 71},
            {"month": "2023-12", "weight_loss_success": 62, "bp_control": 75, "glucose_control": 68},
            {"month": "2023-11", "weight_loss_success": 58, "bp_control": 72, "glucose_control": 65}
        ],
        "risk_stratification": {
            "low_risk": 89,
            "moderate_risk": 124,
            "high_risk": 34
        }
    }

@api_router.post("/provider/treatment-plan")
async def create_treatment_plan(plan_data: dict):
    """Create evidence-based treatment plans"""
    return {
        "success": True,
        "plan_id": str(uuid.uuid4()),
        "patient_id": plan_data.get("patient_id"),
        "provider_id": plan_data.get("provider_id"),
        "recommendations": [
            {
                "category": "nutrition",
                "intervention": "Mediterranean Diet Pattern",
                "evidence_level": "A",
                "duration": "12 weeks",
                "monitoring": "Weekly food logs, monthly weight"
            },
            {
                "category": "physical_activity",
                "intervention": "Progressive Resistance Training",
                "evidence_level": "A",
                "duration": "16 weeks",
                "monitoring": "Bi-weekly fitness assessments"
            }
        ],
        "expected_outcomes": [
            "5-10% weight reduction in 6 months",
            "Improved insulin sensitivity",
            "Reduced cardiovascular risk markers"
        ],
        "follow_up_schedule": [
            {"week": 2, "type": "phone_check", "focus": "diet_adherence"},
            {"week": 4, "type": "office_visit", "focus": "progress_assessment"},
            {"week": 8, "type": "lab_work", "focus": "biomarker_monitoring"}
        ]
    }

# Family Coordination Endpoints
@api_router.get("/family/health-overview/{family_id}")
async def get_family_health_overview(family_id: str):
    """Get comprehensive family health coordination data"""
    return {
        "family_id": family_id,
        "multi_member_tracking": {
            "total_members": 4,
            "health_status": {
                "excellent": 2,
                "good": 1,
                "needs_attention": 1
            },
            "upcoming_appointments": [
                {"member": "Emma", "date": "2024-01-18", "type": "Pediatric Checkup", "provider": "Dr. Smith"},
                {"member": "John", "date": "2024-01-25", "type": "Annual Physical", "provider": "Dr. Johnson"}
            ]
        },
        "shared_goals": [
            {
                "id": "goal_1",
                "title": "Family Fitness Challenge",
                "type": "physical_activity",
                "target": "150 minutes/week per member",
                "current_progress": 75,
                "participants": ["John", "Sarah", "Emma", "Alex"],
                "end_date": "2024-02-15"
            },
            {
                "id": "goal_2",
                "title": "Healthy Eating Habits",
                "type": "nutrition",
                "target": "5 servings fruits/vegetables daily",
                "current_progress": 60,
                "participants": ["John", "Sarah", "Emma", "Alex"],
                "end_date": "2024-01-31"
            }
        ],
        "meal_coordination": {
            "dietary_restrictions": {
                "Emma": ["tree_nuts"],
                "Alex": ["lactose_intolerant"],
                "Sarah": ["gluten_free"],
                "John": ["none"]
            },
            "family_friendly_meals": [
                {"name": "Gluten-Free Chicken Stir Fry", "accommodates": ["Sarah"], "nutrition_score": 9},
                {"name": "Dairy-Free Pasta Primavera", "accommodates": ["Alex"], "nutrition_score": 8},
                {"name": "Nut-Free Trail Mix", "accommodates": ["Emma"], "nutrition_score": 7}
            ],
            "weekly_meal_success": 85
        },
        "care_coordination": {
            "emergency_contacts": [
                {"name": "Grandma Betty", "relationship": "Grandmother", "phone": "+1-555-0123"},
                {"name": "Uncle Mike", "relationship": "Uncle", "phone": "+1-555-0456"}
            ],
            "healthcare_providers": {
                "family_physician": {"name": "Dr. Johnson", "phone": "+1-555-0789"},
                "pediatrician": {"name": "Dr. Smith", "phone": "+1-555-0012"},
                "emergency": {"name": "City Hospital", "phone": "911"}
            },
            "medication_schedule": [
                {"member": "Sarah", "medication": "Multivitamin", "time": "8:00 AM", "frequency": "daily"},
                {"member": "Emma", "medication": "Allergy Medication", "time": "7:00 PM", "frequency": "as_needed"}
            ]
        }
    }

@api_router.get("/family/meal-planning-advanced/{family_id}")
async def get_advanced_meal_planning(family_id: str):
    """Get intelligent meal planning for families"""
    return {
        "family_id": family_id,
        "smart_meal_suggestions": [
            {
                "meal": "Breakfast - Overnight Oats Bar",
                "accommodates_all": True,
                "prep_time": 15,
                "nutrition_score": 9,
                "kid_friendly": True,
                "dietary_notes": "Gluten-free oats, dairy-free milk options, nut-free toppings"
            },
            {
                "meal": "Lunch - Build-Your-Own Salad",
                "accommodates_all": True,
                "prep_time": 10,
                "nutrition_score": 10,
                "kid_friendly": True,
                "dietary_notes": "Customizable for all restrictions"
            }
        ],
        "budget_optimization": {
            "weekly_budget": 150,
            "current_plan_cost": 125,
            "savings_suggestions": [
                "Buy seasonal vegetables - save $15/week",
                "Bulk buy grains and legumes - save $8/week",
                "Plan leftovers strategically - save $12/week"
            ]
        },
        "nutrition_education": [
            {
                "topic": "Growing Bodies Need Protein",
                "age_group": "8-12 years",
                "key_points": ["Protein helps muscle development", "Include protein in every meal", "Fun protein sources: Greek yogurt, eggs, lean meats"],
                "activities": ["Protein scavenger hunt", "Build a balanced plate game"]
            },
            {
                "topic": "Calcium for Strong Bones",
                "age_group": "all",
                "key_points": ["Dairy alternatives for lactose intolerant", "Dark leafy greens are calcium-rich", "Vitamin D helps calcium absorption"],
                "activities": ["Calcium content comparison", "Bone health family challenge"]
            }
        ],
        "meal_prep_coordination": {
            "sunday_prep": [
                {"task": "Wash and chop vegetables", "assigned_to": "Sarah", "time": "30 min"},
                {"task": "Cook grains in bulk", "assigned_to": "John", "time": "45 min"},
                {"task": "Prepare snack portions", "assigned_to": "Emma & Alex", "time": "20 min"}
            ],
            "daily_assignments": {
                "monday": {"cook": "Sarah", "cleanup": "John", "help": "Emma"},
                "tuesday": {"cook": "John", "cleanup": "Sarah", "help": "Alex"}
            }
        }
    }

# Guest Experience Endpoints
@api_router.get("/guest/quick-nutrition/{session_id}")
async def get_guest_quick_nutrition(session_id: str):
    """Get instant nutrition insights for guest users"""
    return {
        "session_id": session_id,
        "instant_calculations": {
            "estimated_bmr": 1650,
            "daily_calorie_needs": 2100,
            "protein_needs": "84-126g",
            "fiber_needs": "25g",
            "water_needs": "8-10 glasses"
        },
        "quick_assessments": [
            {
                "category": "hydration",
                "current_status": "adequate",
                "recommendation": "Maintain current water intake",
                "simple_tips": ["Drink a glass of water before each meal", "Keep a water bottle visible"]
            },
            {
                "category": "energy",
                "current_status": "good",
                "recommendation": "Include protein in every meal",
                "simple_tips": ["Add Greek yogurt to smoothies", "Include nuts or seeds as snacks"]
            }
        ],
        "educational_content": [
            {
                "topic": "Reading Nutrition Labels",
                "level": "beginner",
                "key_points": ["Look at serving size first", "Check sugar content", "Aim for more fiber"],
                "time_to_read": "3 minutes"
            },
            {
                "topic": "Portion Control Basics",
                "level": "beginner",
                "key_points": ["Use your hand as a guide", "Fill half plate with vegetables", "Protein = palm size"],
                "time_to_read": "2 minutes"
            }
        ],
        "upgrade_benefits": [
            "Save your food preferences and get personalized recommendations",
            "Track your progress over time with detailed analytics",
            "Get custom meal plans based on your goals and dietary needs",
            "Access to expert-reviewed nutrition content and recipes"
        ]
    }

@api_router.post("/guest/instant-food-log")
async def instant_guest_food_log(food_data: dict):
    """Instant food logging for guests with immediate feedback"""
    return {
        "success": True,
        "food_recognized": food_data.get("food_name", "Unknown Food"),
        "estimated_nutrition": {
            "calories": food_data.get("calories", 200),
            "protein": 15,
            "carbs": 25,
            "fat": 8,
            "fiber": 3
        },
        "instant_feedback": [
            "Good choice! This food provides quality protein for sustained energy.",
            "Consider adding some vegetables or fruits to boost fiber and vitamins.",
            "This fits well within a balanced 2000-calorie daily plan."
        ],
        "session_totals": {
            "today_calories": 580,
            "meals_logged": 2,
            "session_time": "12 minutes"
        },
        "simple_suggestions": [
            "Try pairing this with a small salad for extra nutrients",
            "A glass of water now will help with digestion",
            "This makes a great base - add some colorful vegetables!"
        ],
        "learning_moment": {
            "tip": "Did you know?",
            "content": "Protein helps you feel full longer and supports muscle health. Aim for some protein in every meal!"
        }
    }

# Role-Based Data Access Endpoints
@api_router.get("/roles/{role}/features")
async def get_role_features(role: str):
    """Get available features for specific role"""
    role_features = {
        "patient": [
            {"name": "Personal Health Analytics", "category": "analytics", "premium": False},
            {"name": "Smart Food Logging", "category": "tracking", "premium": False},
            {"name": "Health Goal Tracking", "category": "goals", "premium": False},
            {"name": "Symptom Correlation", "category": "insights", "premium": True},
            {"name": "AI Health Insights", "category": "ai", "premium": True},
            {"name": "Medication Reminders", "category": "health", "premium": True}
        ],
        "provider": [
            {"name": "Patient Management", "category": "clinical", "premium": False},
            {"name": "Clinical Decision Support", "category": "clinical", "premium": True},
            {"name": "Population Health Analytics", "category": "analytics", "premium": True},
            {"name": "Evidence-Based Recommendations", "category": "clinical", "premium": True},
            {"name": "Treatment Outcome Tracking", "category": "tracking", "premium": False}
        ],
        "family": [
            {"name": "Multi-Profile Management", "category": "coordination", "premium": False},
            {"name": "Family Meal Planning", "category": "nutrition", "premium": False},
            {"name": "Care Coordination", "category": "health", "premium": False},
            {"name": "Child Nutrition Education", "category": "education", "premium": True},
            {"name": "Family Health Analytics", "category": "analytics", "premium": True}
        ],
        "guest": [
            {"name": "Quick Nutrition Tracking", "category": "tracking", "premium": False},
            {"name": "Basic Health Calculations", "category": "tools", "premium": False},
            {"name": "Nutrition Education", "category": "education", "premium": False},
            {"name": "Simple Goal Setting", "category": "goals", "premium": False}
        ]
    }
    
    return {
        "role": role,
        "features": role_features.get(role, []),
        "feature_count": len(role_features.get(role, [])),
        "premium_features": len([f for f in role_features.get(role, []) if f.get("premium", False)])
    }

@api_router.get("/analytics/role-usage")
async def get_role_usage_analytics():
    """Get usage analytics across all roles"""
    return {
        "total_users": 1247,
        "role_distribution": {
            "patient": {"count": 892, "percentage": 71.5, "growth": 12.3},
            "provider": {"count": 45, "percentage": 3.6, "growth": 8.9},
            "family": {"count": 234, "percentage": 18.8, "growth": 15.7},
            "guest": {"count": 76, "percentage": 6.1, "growth": -2.1}
        },
        "feature_usage": {
            "most_used": [
                {"feature": "Food Logging", "usage": 89.2, "role": "patient"},
                {"feature": "Family Meal Planning", "usage": 76.8, "role": "family"},
                {"feature": "Patient Management", "usage": 92.1, "role": "provider"}
            ],
            "emerging": [
                {"feature": "Symptom Correlation", "growth": 45.2, "role": "patient"},
                {"feature": "Population Analytics", "growth": 38.7, "role": "provider"}
            ]
        },
        "engagement_metrics": {
            "daily_active_users": 567,
            "weekly_retention": 78.4,
            "monthly_retention": 65.2,
            "average_session_time": "23 minutes"
        }
    }

# Session Management for Guests
@api_router.post("/guest/session")
async def create_guest_session():
    """Create a new guest session"""
    session_id = f"guest_{int(datetime.utcnow().timestamp())}_{uuid.uuid4().hex[:8]}"
    return {
        "session_id": session_id,
        "expires_at": (datetime.utcnow().timestamp() + 86400),  # 24 hours
        "features_available": [
            "instant_food_logging",
            "basic_nutrition_info",
            "simple_goal_tracking",
            "educational_content"
        ],
        "limitations": [
            "Data not permanently stored",
            "Limited to basic features",
            "No historical tracking",
            "No personalized recommendations"
        ],
        "upgrade_benefits": [
            "Permanent data storage",
            "Advanced analytics",
            "Personalized insights",
            "Goal tracking over time"
        ]
    }

@api_router.get("/guest/session/{session_id}/status")
async def get_guest_session_status(session_id: str):
    """Check guest session status and activity"""
    return {
        "session_id": session_id,
        "status": "active",
        "time_remaining": "18h 32m",
        "activity_summary": {
            "foods_logged": 5,
            "tips_viewed": 3,
            "calculations_used": 2,
            "session_duration": "15m 23s"
        },
        "recommendations": [
            "You're doing great! Consider setting a simple daily goal.",
            "Try logging your dinner to get a complete daily picture.",
            "Check out our nutrition tips section for more insights."
        ]
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
