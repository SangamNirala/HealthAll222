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
from datetime import datetime, timedelta
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

# PHASE 4: Advanced Provider Features

@api_router.get("/provider/patient-queue/{provider_id}")
async def get_patient_queue(provider_id: str):
    """Patient Queue Management System"""
    return {
        "provider_id": provider_id,
        "queue_stats": {
            "total_in_queue": 12,
            "urgent": 3,
            "scheduled": 8,
            "walk_in": 1,
            "avg_wait_time": "18 minutes"
        },
        "priority_queue": [
            {
                "id": "urgent-001",
                "patient_name": "Maria Rodriguez",
                "condition": "Chest pain",
                "priority": "urgent",
                "wait_time": "5 minutes",
                "room": "ER-3",
                "vitals": {"bp": "160/95", "hr": "105", "temp": "98.6°F"},
                "status": "ready_for_provider"
            },
            {
                "id": "urgent-002", 
                "patient_name": "Robert Chen",
                "condition": "Diabetic emergency",
                "priority": "urgent",
                "wait_time": "12 minutes",
                "room": "Room 5",
                "vitals": {"bp": "145/88", "hr": "92", "glucose": "280"},
                "status": "vitals_taken"
            }
        ],
        "scheduled_queue": [
            {
                "id": "sched-001",
                "patient_name": "Sarah Johnson",
                "appointment_time": "2:00 PM",
                "condition": "Routine follow-up",
                "priority": "routine",
                "wait_time": "on_time",
                "room": "Room 2",
                "status": "checked_in"
            },
            {
                "id": "sched-002",
                "patient_name": "David Wilson",
                "appointment_time": "2:30 PM", 
                "condition": "Medication review",
                "priority": "routine",
                "wait_time": "early",
                "room": "waiting",
                "status": "waiting"
            }
        ],
        "completed_today": 8,
        "no_shows": 1
    }

@api_router.post("/provider/clinical-decision-support")
async def clinical_decision_support(request: dict):
    """AI-Powered Clinical Decision Support"""
    patient_data = request.get("patient_data", {})
    symptoms = request.get("symptoms", [])
    history = request.get("history", [])
    
    # This would integrate with AI service for real recommendations
    return {
        "request_id": f"cds-{uuid.uuid4().hex[:8]}",
        "patient_id": patient_data.get("id", "unknown"),
        "ai_recommendations": [
            {
                "category": "diagnosis",
                "confidence": 0.87,
                "recommendation": "Consider Type 2 Diabetes screening based on symptoms",
                "evidence": "Patient presents with classic triad: polyuria, polydipsia, and unexplained weight loss",
                "next_steps": ["Order HbA1c", "Fasting glucose test", "Consider glucose tolerance test"]
            },
            {
                "category": "treatment",
                "confidence": 0.92,
                "recommendation": "Lifestyle modifications as first-line intervention",
                "evidence": "Evidence-based guidelines support lifestyle changes for pre-diabetes prevention",
                "next_steps": ["Dietary counseling", "Exercise prescription", "Weight management plan"]
            }
        ],
        "drug_interactions": [],
        "contraindications": [],
        "clinical_guidelines": [
            {
                "guideline": "ADA Standards of Medical Care 2024",
                "recommendation": "Screen adults ≥45 years for diabetes every 3 years",
                "relevance": "high"
            }
        ],
        "risk_scores": {
            "diabetes_risk": 0.73,
            "cardiovascular_risk": 0.41,
            "overall_risk": "moderate"
        }
    }

@api_router.get("/provider/treatment-outcomes/{provider_id}")
async def get_treatment_outcomes(provider_id: str, timeframe: str = "30d"):
    """Treatment Outcome Tracking"""
    return {
        "provider_id": provider_id,
        "timeframe": timeframe,
        "outcome_summary": {
            "total_patients_treated": 156,
            "successful_outcomes": 134,
            "success_rate": 85.9,
            "readmission_rate": 4.2,
            "patient_satisfaction": 4.7
        },
        "condition_outcomes": [
            {
                "condition": "Type 2 Diabetes",
                "patients": 45,
                "improved": 38,
                "stable": 5,
                "declined": 2,
                "avg_hba1c_reduction": 1.2,
                "target_achievement_rate": 84.4
            },
            {
                "condition": "Hypertension",
                "patients": 62,
                "improved": 48,
                "stable": 12,
                "declined": 2,
                "avg_bp_reduction": "15/8 mmHg",
                "target_achievement_rate": 77.4
            },
            {
                "condition": "Obesity",
                "patients": 33,
                "improved": 28,
                "stable": 4,
                "declined": 1,
                "avg_weight_loss": 12.3,
                "target_achievement_rate": 84.8
            }
        ],
        "trending_metrics": [
            {
                "metric": "HbA1c Control",
                "current": 84.4,
                "previous": 78.2,
                "trend": "improving",
                "change": "+6.2%"
            },
            {
                "metric": "Blood Pressure Control",
                "current": 77.4,
                "previous": 74.1,
                "trend": "improving", 
                "change": "+3.3%"
            }
        ]
    }

@api_router.get("/provider/population-health/{provider_id}")
async def get_population_health(provider_id: str):
    """Population Health Analytics"""
    return {
        "provider_id": provider_id,
        "population_overview": {
            "total_population": 2847,
            "active_patients": 2156,
            "high_risk_patients": 284,
            "chronic_conditions_prevalence": 45.2
        },
        "demographic_breakdown": [
            {"age_group": "18-35", "count": 542, "percentage": 19.0, "top_conditions": ["Anxiety", "Depression"]},
            {"age_group": "36-50", "count": 896, "percentage": 31.5, "top_conditions": ["Hypertension", "Diabetes"]},
            {"age_group": "51-65", "count": 758, "percentage": 26.6, "top_conditions": ["Diabetes", "Heart Disease"]},
            {"age_group": "65+", "count": 651, "percentage": 22.9, "top_conditions": ["Heart Disease", "Arthritis"]}
        ],
        "condition_prevalence": [
            {"condition": "Hypertension", "count": 567, "prevalence": 19.9, "trend": "stable"},
            {"condition": "Type 2 Diabetes", "count": 423, "prevalence": 14.9, "trend": "increasing"},
            {"condition": "Obesity", "count": 398, "prevalence": 14.0, "trend": "increasing"},
            {"condition": "Heart Disease", "count": 278, "prevalence": 9.8, "trend": "stable"},
            {"condition": "Depression", "count": 234, "prevalence": 8.2, "trend": "increasing"}
        ],
        "risk_stratification": {
            "low_risk": {"count": 1698, "percentage": 59.7},
            "medium_risk": {"count": 865, "percentage": 30.4},
            "high_risk": {"count": 284, "percentage": 9.9}
        },
        "quality_measures": [
            {
                "measure": "Diabetes HbA1c Control",
                "target": ">80%",
                "current": "84.2%",
                "status": "meeting_target"
            },
            {
                "measure": "Blood Pressure Control",
                "target": ">75%", 
                "current": "77.8%",
                "status": "meeting_target"
            },
            {
                "measure": "Preventive Screening",
                "target": ">90%",
                "current": "67.3%",
                "status": "below_target"
            }
        ],
        "intervention_opportunities": [
            {
                "intervention": "Diabetes Prevention Program",
                "eligible_patients": 156,
                "potential_impact": "23% risk reduction",
                "priority": "high"
            },
            {
                "intervention": "Hypertension Management",
                "eligible_patients": 89,
                "potential_impact": "15% cardiovascular risk reduction",
                "priority": "medium"
            }
        ]
    }

@api_router.post("/provider/evidence-recommendations")
async def get_evidence_recommendations(request: dict):
    """AI-Powered Evidence-Based Recommendations"""
    condition = request.get("condition", "")
    patient_profile = request.get("patient_profile", {})
    clinical_context = request.get("clinical_context", "")
    
    # This would integrate with AI service for real evidence-based recommendations
    return {
        "request_id": f"ebr-{uuid.uuid4().hex[:8]}",
        "condition": condition,
        "evidence_level": "high",
        "recommendations": [
            {
                "category": "first_line_treatment",
                "recommendation": "Metformin monotherapy",
                "evidence_level": "A",
                "source": "ADA 2024 Standards of Care",
                "dosing": "Start 500mg BID, titrate to 1000mg BID",
                "monitoring": "Monitor renal function, B12 levels",
                "contraindications": ["eGFR <30", "Acute heart failure"],
                "confidence": 0.94
            },
            {
                "category": "lifestyle_intervention",
                "recommendation": "Structured lifestyle program",
                "evidence_level": "A",
                "source": "Diabetes Prevention Program",
                "details": "7% weight loss goal, 150 min/week moderate exercise",
                "expected_outcome": "58% diabetes risk reduction",
                "confidence": 0.96
            }
        ],
        "clinical_studies": [
            {
                "study": "UKPDS",
                "year": "1998",
                "finding": "Intensive glucose control reduces microvascular complications",
                "relevance": "high",
                "patient_count": 3867
            }
        ],
        "contraindications": [],
        "drug_interactions": [],
        "patient_specific_factors": [
            {
                "factor": "Age > 65",
                "implication": "Consider lower starting dose",
                "adjustment": "Start metformin 250mg BID"
            }
        ],
        "follow_up_recommendations": [
            "Reassess in 3 months",
            "Monitor HbA1c quarterly",
            "Annual eye exam",
            "Quarterly foot exam"
        ]
    }

@api_router.get("/provider/continuing-education/{provider_id}")
async def get_continuing_education(provider_id: str):
    """Professional Continuing Education Portal"""
    return {
        "provider_id": provider_id,
        "education_summary": {
            "total_credits_earned": 32.5,
            "credits_required": 50.0,
            "progress_percentage": 65.0,
            "courses_completed": 8,
            "courses_in_progress": 3,
            "deadline": "2024-12-31"
        },
        "featured_courses": [
            {
                "id": "course-001",
                "title": "Advanced Diabetes Management 2024",
                "provider": "American Diabetes Association", 
                "credits": 4.0,
                "duration": "4 hours",
                "format": "Online",
                "difficulty": "Intermediate",
                "rating": 4.8,
                "enrolled": False,
                "cost": "Free",
                "description": "Latest evidence-based approaches to diabetes care",
                "learning_objectives": [
                    "Apply 2024 ADA guidelines",
                    "Optimize medication regimens",
                    "Implement technology solutions"
                ]
            },
            {
                "id": "course-002",
                "title": "Population Health Strategies",
                "provider": "CDC",
                "credits": 3.5,
                "duration": "3.5 hours",
                "format": "Webinar",
                "difficulty": "Advanced",
                "rating": 4.6,
                "enrolled": True,
                "progress": 60,
                "cost": "Free",
                "description": "Community-based interventions for chronic disease"
            }
        ],
        "my_courses": [
            {
                "id": "course-003",
                "title": "Nutrition Counseling Essentials",
                "status": "in_progress",
                "progress": 75,
                "credits": 2.5,
                "due_date": "2024-02-15",
                "last_accessed": "2024-01-10"
            },
            {
                "id": "course-004", 
                "title": "Clinical Documentation",
                "status": "completed",
                "progress": 100,
                "credits": 3.0,
                "completed_date": "2023-12-20",
                "certificate_url": "/certificates/course-004.pdf"
            }
        ],
        "categories": [
            {"id": "diabetes", "name": "Diabetes Care", "course_count": 15},
            {"id": "cardiology", "name": "Cardiovascular Health", "course_count": 12},
            {"id": "nutrition", "name": "Nutrition & Dietetics", "course_count": 18},
            {"id": "mental_health", "name": "Mental Health", "course_count": 9},
            {"id": "technology", "name": "Health Technology", "course_count": 7}
        ],
        "upcoming_deadlines": [
            {"course": "Nutrition Counseling Essentials", "due_date": "2024-02-15", "days_left": 6},
            {"course": "Annual CME Requirement", "due_date": "2024-12-31", "days_left": 330}
        ]
    }

@api_router.post("/provider/courses/{course_id}/enroll")
async def enroll_in_course(course_id: str, provider_id: str = Body(...)):
    """Enroll in a continuing education course"""
    return {
        "course_id": course_id,
        "provider_id": provider_id,
        "enrollment_status": "success",
        "message": "Successfully enrolled in course",
        "access_url": f"/courses/{course_id}/learn",
        "enrollment_date": "2024-01-15"
    }

@api_router.get("/provider/certificates/{provider_id}")
async def get_certificates(provider_id: str):
    """Get earned certificates"""
    return {
        "provider_id": provider_id,
        "certificates": [
            {
                "id": "cert-001",
                "course_title": "Advanced Diabetes Management",
                "credits": 4.0,
                "completed_date": "2023-11-15",
                "certificate_number": "ADM-2023-001",
                "download_url": "/certificates/cert-001.pdf",
                "verification_code": "ADM4B7X9"
            },
            {
                "id": "cert-002",
                "course_title": "Clinical Documentation", 
                "credits": 3.0,
                "completed_date": "2023-12-20",
                "certificate_number": "CD-2023-002",
                "download_url": "/certificates/cert-002.pdf",
                "verification_code": "CD8K2M5P"
            }
        ],
        "total_credits": 32.5
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
        # ai_insights = await get_nutrition_insights(user_data)
        ai_insights = {"insights": [], "recommendations": [], "confidence": 0.0}
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
        # ai_correlations = await get_health_correlations(health_data)
        ai_correlations = {"correlations": []}
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
        # ai_suggestions = await get_smart_food_suggestions(user_profile, current_intake)
        ai_suggestions = []
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

# PHASE 5: Comprehensive Family Features - Advanced APIs

@api_router.get("/family/calendar-integration/{family_id}")
async def get_family_calendar_integration(family_id: str):
    """Advanced family calendar with health events coordination"""
    return {
        "family_id": family_id,
        "calendar_overview": {
            "this_week_events": [
                {
                    "id": "evt_1",
                    "title": "Emma - Pediatric Annual Checkup",
                    "date": "2024-01-18",
                    "time": "2:30 PM",
                    "type": "medical_appointment",
                    "member": "Emma",
                    "provider": "Dr. Smith",
                    "location": "Children's Clinic",
                    "preparation_needed": ["Bring insurance card", "List of current medications", "Growth chart"],
                    "reminders_set": True
                },
                {
                    "id": "evt_2", 
                    "title": "Family Meal Prep Day",
                    "date": "2024-01-20",
                    "time": "10:00 AM",
                    "type": "meal_prep",
                    "participants": ["Sarah", "John", "Emma", "Alex"],
                    "planned_meals": ["Overnight oats", "Chicken stir fry", "Veggie muffins"],
                    "shopping_completed": True
                },
                {
                    "id": "evt_3",
                    "title": "Alex - Soccer Practice",
                    "date": "2024-01-21",
                    "time": "4:30 PM", 
                    "type": "physical_activity",
                    "member": "Alex",
                    "location": "Community Sports Center",
                    "health_benefits": ["cardiovascular health", "teamwork", "coordination"],
                    "hydration_reminder": True
                }
            ],
            "upcoming_medical": [
                {"member": "John", "appointment": "Annual Physical", "date": "2024-01-25", "status": "confirmed"},
                {"member": "Sarah", "appointment": "Nutritionist Consultation", "date": "2024-02-01", "status": "tentative"},
                {"member": "Emma", "appointment": "Orthodontist Follow-up", "date": "2024-02-08", "status": "confirmed"}
            ],
            "medication_schedule": {
                "daily_reminders": [
                    {"member": "Sarah", "medication": "Prenatal Vitamin", "time": "8:00 AM", "status": "active"},
                    {"member": "Emma", "medication": "Allergy Medication", "time": "7:00 PM", "condition": "seasonal allergies", "status": "as_needed"}
                ],
                "upcoming_refills": [
                    {"member": "Emma", "medication": "Allergy Medication", "refill_due": "2024-01-30", "pharmacy": "Main Street Pharmacy"}
                ]
            }
        },
        "synchronization": {
            "google_calendar": {"connected": True, "last_sync": "2024-01-17 6:00 AM"},
            "apple_calendar": {"connected": False, "available": True},
            "outlook_calendar": {"connected": False, "available": True}
        },
        "family_coordination": {
            "shared_responsibilities": [
                {"task": "Take Emma to checkup", "assigned_to": "Sarah", "date": "2024-01-18", "backup": "John"},
                {"task": "Pick up prescriptions", "assigned_to": "John", "date": "2024-01-19", "backup": "Sarah"}
            ],
            "transportation_coordination": [
                {"event": "Emma's Checkup", "driver": "Sarah", "passengers": ["Emma"], "departure_time": "2:00 PM"},
                {"event": "Alex's Soccer", "driver": "John", "passengers": ["Alex"], "departure_time": "4:00 PM"}
            ]
        }
    }

@api_router.get("/family/child-nutrition-education/{family_id}")
async def get_child_nutrition_education(family_id: str):
    """Comprehensive child nutrition education portal"""
    return {
        "family_id": family_id,
        "age_specific_content": [
            {
                "age_group": "8-10 years (Alex)",
                "learning_modules": [
                    {
                        "title": "Super Foods for Super Kids",
                        "duration": "15 minutes",
                        "type": "interactive_game",
                        "concepts": ["protein for muscles", "calcium for bones", "vitamins for energy"],
                        "activities": ["Food superhero matching", "Build a power plate", "Nutrient scavenger hunt"],
                        "completion_badge": "Nutrition Detective",
                        "progress": 60
                    },
                    {
                        "title": "Reading Food Labels Like a Pro", 
                        "duration": "10 minutes",
                        "type": "tutorial_video",
                        "concepts": ["serving sizes", "sugar content", "ingredient lists"],
                        "activities": ["Label detective game", "Compare similar foods", "Make healthy swaps"],
                        "completion_badge": "Label Reader",
                        "progress": 0
                    }
                ],
                "dietary_considerations": ["lactose_intolerant", "high_energy_needs", "growing_body"],
                "recommended_portions": {
                    "proteins": "2-3 servings/day",
                    "vegetables": "3-4 servings/day", 
                    "fruits": "2-3 servings/day",
                    "grains": "4-5 servings/day",
                    "dairy_alternatives": "2-3 servings/day"
                }
            },
            {
                "age_group": "12-14 years (Emma)",
                "learning_modules": [
                    {
                        "title": "Fueling Your Growing Body",
                        "duration": "20 minutes", 
                        "type": "interactive_workshop",
                        "concepts": ["adolescent nutrition needs", "body image positivity", "sports nutrition"],
                        "activities": ["Plan a perfect day of eating", "Myth vs fact quiz", "Energy balance calculator"],
                        "completion_badge": "Teen Nutrition Expert",
                        "progress": 30
                    },
                    {
                        "title": "Cooking Skills for Independence",
                        "duration": "25 minutes",
                        "type": "hands_on_cooking",
                        "concepts": ["meal preparation", "food safety", "balanced cooking"],
                        "activities": ["Cook a balanced meal", "Grocery shopping simulation", "Recipe modification"],
                        "completion_badge": "Young Chef",
                        "progress": 80
                    }
                ],
                "dietary_considerations": ["tree_nuts_allergy", "adolescent_growth", "active_lifestyle"],
                "recommended_portions": {
                    "proteins": "3-4 servings/day",
                    "vegetables": "4-5 servings/day",
                    "fruits": "3-4 servings/day", 
                    "grains": "6-7 servings/day",
                    "healthy_fats": "2-3 servings/day"
                }
            }
        ],
        "family_challenges": [
            {
                "name": "Rainbow Plate Challenge",
                "description": "Eat foods of every color each day for a week",
                "duration": "7 days",
                "participants": ["Emma", "Alex"],
                "progress": {"Emma": 85, "Alex": 70},
                "rewards": ["Healthy cooking class", "Family day out", "New sports equipment"]
            },
            {
                "name": "Hydration Heroes",
                "description": "Track water intake and learn about hydration", 
                "duration": "10 days",
                "participants": ["Emma", "Alex", "Sarah", "John"],
                "progress": {"Emma": 90, "Alex": 65, "Sarah": 100, "John": 80},
                "rewards": ["Family water bottles", "Healthy smoothie making", "Spa day"]
            }
        ],
        "expert_resources": [
            {
                "title": "Pediatric Nutritionist Q&A",
                "type": "live_session", 
                "date": "2024-01-25",
                "time": "7:00 PM",
                "expert": "Dr. Lisa Chen, RD",
                "topics": ["Picky eating", "Food allergies", "Growth nutrition"],
                "registration_required": True
            },
            {
                "title": "Family Cooking Workshop",
                "type": "hands_on_class",
                "date": "2024-02-03",
                "time": "2:00 PM", 
                "location": "Community Kitchen",
                "instructor": "Chef Maria Rodriguez",
                "focus": "Allergen-free family meals",
                "age_range": "8+ with parent"
            }
        ]
    }

@api_router.get("/family/caregiver-tools/{family_id}")
async def get_advanced_caregiver_tools(family_id: str):
    """Advanced caregiver tools and emergency management"""
    return {
        "family_id": family_id,
        "emergency_management": {
            "emergency_contacts": [
                {
                    "name": "Grandma Betty",
                    "relationship": "Grandmother", 
                    "phone": "+1-555-0123",
                    "availability": "weekdays 9AM-6PM",
                    "medical_authority": True,
                    "key_holder": True,
                    "special_instructions": "Knows Emma's allergy protocol"
                },
                {
                    "name": "Uncle Mike",
                    "relationship": "Uncle",
                    "phone": "+1-555-0456", 
                    "availability": "weekends and evenings",
                    "medical_authority": False,
                    "key_holder": True,
                    "special_instructions": "Lives 5 minutes away, has backup car seats"
                },
                {
                    "name": "Neighbor Jane",
                    "relationship": "Neighbor",
                    "phone": "+1-555-0789",
                    "availability": "emergencies only",
                    "medical_authority": False,
                    "key_holder": False,
                    "special_instructions": "Retired nurse, great in medical emergencies"
                }
            ],
            "medical_information": {
                "Emma": {
                    "allergies": ["tree nuts", "severe"],
                    "medications": ["EpiPen - always carry", "Allergy medication - as needed"],
                    "medical_conditions": ["Seasonal allergies"],
                    "emergency_protocols": ["Use EpiPen immediately for nut exposure", "Call 911", "Contact parents"],
                    "insurance": {"provider": "Blue Cross", "policy": "XYZ123", "group": "FAM001"}
                },
                "Alex": {
                    "allergies": ["none known"],
                    "medications": ["none regular"],
                    "medical_conditions": ["Lactose intolerant"],
                    "emergency_protocols": ["Standard emergency care", "Avoid dairy products"],
                    "insurance": {"provider": "Blue Cross", "policy": "XYZ123", "group": "FAM001"}
                }
            },
            "healthcare_providers": {
                "primary_care": {"name": "Dr. Johnson", "phone": "+1-555-0100", "available": "24/7 on-call"},
                "pediatrician": {"name": "Dr. Smith", "phone": "+1-555-0200", "available": "Mon-Fri 8AM-6PM"},
                "emergency": {"name": "City Hospital ER", "phone": "911", "address": "123 Medical Center Dr"},
                "urgent_care": {"name": "QuickCare Clinic", "phone": "+1-555-0300", "available": "7AM-11PM daily"}
            }
        },
        "medication_management": {
            "current_medications": [
                {
                    "member": "Sarah",
                    "medication": "Prenatal Vitamin",
                    "dosage": "1 tablet daily",
                    "time": "8:00 AM",
                    "refill_date": "2024-02-15",
                    "pharmacy": "Main Street Pharmacy",
                    "reminder_enabled": True,
                    "side_effects_to_watch": ["nausea", "constipation"]
                },
                {
                    "member": "Emma", 
                    "medication": "EpiPen",
                    "dosage": "0.3mg auto-injector",
                    "condition": "severe tree nut allergy",
                    "location": ["backpack", "home", "car"],
                    "expiration_date": "2024-08-15",
                    "replacement_reminder": True,
                    "training_needed": ["How to use", "When to use", "After-care steps"]
                }
            ],
            "medication_adherence": {
                "Sarah": {"compliance_rate": 95, "missed_doses": 2, "streak": 28},
                "Emma": {"compliance_rate": 100, "missed_doses": 0, "streak": 45}
            },
            "refill_management": [
                {"medication": "Prenatal Vitamin", "due_date": "2024-02-15", "auto_refill": True, "status": "scheduled"},
                {"medication": "EpiPen", "due_date": "2024-07-15", "auto_refill": False, "status": "reminder_set"}
            ]
        },
        "care_coordination": {
            "shared_tasks": [
                {"task": "Daily medication check", "assigned_to": "Sarah", "backup": "John", "frequency": "daily"},
                {"task": "Weekly health check-ins", "assigned_to": "alternating", "frequency": "weekly"},
                {"task": "Medical appointment scheduling", "assigned_to": "Sarah", "backup": "John", "frequency": "as_needed"}
            ],
            "communication_hub": {
                "family_chat": {"enabled": True, "platform": "secure_messaging", "participants": ["Sarah", "John"]},
                "provider_communication": {"enabled": True, "secure_portal": True, "recent_messages": 3},
                "school_nurse_contact": {"name": "Nurse Patricia", "phone": "+1-555-0400", "email": "patricia@school.edu"}
            },
            "document_management": {
                "medical_records": {"location": "encrypted_cloud", "last_updated": "2024-01-15", "access": ["Sarah", "John"]},
                "insurance_cards": {"location": "digital_wallet", "backup_printed": True, "expiration": "2024-12-31"},
                "emergency_info_sheets": {"location": "car, home, school", "last_updated": "2024-01-10", "review_due": "2024-07-10"}
            }
        },
        "health_monitoring": {
            "wellness_checks": [
                {"member": "Emma", "type": "allergy_symptom_tracking", "frequency": "daily", "last_entry": "2024-01-17"},
                {"member": "Alex", "type": "growth_monitoring", "frequency": "monthly", "last_entry": "2024-01-01"},
                {"member": "Sarah", "type": "pregnancy_wellness", "frequency": "weekly", "last_entry": "2024-01-16"}
            ],
            "symptom_tracking": {
                "Emma": {
                    "tracked_symptoms": ["sneezing", "itchy_eyes", "congestion"],
                    "triggers": ["tree_pollen", "dust"],
                    "patterns": "Symptoms worse in morning and evening",
                    "improvements": "Better with air purifier in room"
                }
            },
            "growth_tracking": {
                "Alex": {
                    "height": {"current": "4'8\"", "growth_rate": "2 inches/year", "percentile": "75th"},
                    "weight": {"current": "85 lbs", "growth_rate": "healthy", "percentile": "70th"},
                    "next_measurement": "2024-02-01"
                },
                "Emma": {
                    "height": {"current": "5'2\"", "growth_rate": "1 inch/year", "percentile": "60th"},
                    "weight": {"current": "105 lbs", "growth_rate": "healthy", "percentile": "55th"},
                    "next_measurement": "2024-02-01"
                }
            }
        }
    }

@api_router.get("/family/goals-coordination/{family_id}")
async def get_family_goals_coordination(family_id: str):
    """Advanced family goal setting and progress coordination"""
    return {
        "family_id": family_id,
        "active_goals": [
            {
                "id": "goal_nutrition_2024",
                "title": "Balanced Nutrition Challenge",
                "category": "nutrition",
                "description": "Each family member eats 5 servings of fruits and vegetables daily",
                "start_date": "2024-01-01",
                "end_date": "2024-03-31",
                "participants": [
                    {"name": "Sarah", "target": "5 servings/day", "current_progress": 85, "streak": 12},
                    {"name": "John", "target": "5 servings/day", "current_progress": 70, "streak": 8},
                    {"name": "Emma", "target": "4 servings/day", "current_progress": 90, "streak": 15},
                    {"name": "Alex", "target": "4 servings/day", "current_progress": 65, "streak": 5}
                ],
                "family_progress": 77,
                "milestones": [
                    {"week": 2, "achieved": True, "reward": "Family movie night"},
                    {"week": 4, "achieved": True, "reward": "Healthy cooking class"},
                    {"week": 8, "achieved": False, "reward": "Weekend farmer's market trip"},
                    {"week": 12, "achieved": False, "reward": "Family day at the park"}
                ],
                "tracking_method": "daily_photo_journal",
                "support_features": ["meal_suggestions", "progress_charts", "family_leaderboard"]
            },
            {
                "id": "goal_fitness_2024",
                "title": "Family Fitness Adventure",
                "category": "physical_activity",
                "description": "Family participates in physical activities together 4x per week",
                "start_date": "2024-01-01",
                "end_date": "2024-06-30",
                "participants": [
                    {"name": "Sarah", "target": "4 activities/week", "current_progress": 80, "favorite_activity": "hiking"},
                    {"name": "John", "target": "4 activities/week", "current_progress": 75, "favorite_activity": "cycling"},
                    {"name": "Emma", "target": "3 activities/week", "current_progress": 95, "favorite_activity": "dancing"},
                    {"name": "Alex", "target": "4 activities/week", "current_progress": 90, "favorite_activity": "soccer"}
                ],
                "family_progress": 85,
                "weekly_activities": [
                    {"day": "Saturday", "activity": "Family bike ride", "status": "completed", "duration": "45 min"},
                    {"day": "Sunday", "activity": "Park playground", "status": "completed", "duration": "60 min"},
                    {"day": "Wednesday", "activity": "Evening walk", "status": "scheduled", "duration": "30 min"},
                    {"day": "Friday", "activity": "Dance party", "status": "planned", "duration": "20 min"}
                ],
                "health_benefits": ["cardiovascular health", "family_bonding", "stress_reduction", "better_sleep"]
            },
            {
                "id": "goal_wellness_2024",
                "title": "Family Wellness Routine",
                "category": "overall_wellness", 
                "description": "Establish healthy family routines for sleep, hydration, and mindfulness",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "participants": [
                    {"name": "Sarah", "focus_areas": ["sleep_schedule", "hydration", "stress_management"], "progress": 88},
                    {"name": "John", "focus_areas": ["sleep_schedule", "hydration", "work_life_balance"], "progress": 72},
                    {"name": "Emma", "focus_areas": ["sleep_schedule", "screen_time", "study_stress"], "progress": 82},
                    {"name": "Alex", "focus_areas": ["sleep_schedule", "hydration", "emotional_regulation"], "progress": 79}
                ],
                "family_routines": [
                    {
                        "routine": "Digital sunset at 8 PM",
                        "description": "All screens off 1 hour before bedtime",
                        "compliance": 85,
                        "benefits": ["better_sleep", "family_time", "reduced_eye_strain"]
                    },
                    {
                        "routine": "Morning hydration challenge",
                        "description": "Everyone drinks water immediately upon waking",
                        "compliance": 92,
                        "benefits": ["metabolism_boost", "alertness", "healthy_habit"]
                    },
                    {
                        "routine": "Weekly family gratitude circle",
                        "description": "Share three things we're grateful for each Sunday",
                        "compliance": 78,
                        "benefits": ["emotional_wellbeing", "family_connection", "positive_mindset"]
                    }
                ]
            }
        ],
        "goal_analytics": {
            "overall_family_score": 83,
            "improvement_trends": [
                {"metric": "nutrition_consistency", "change": "+15%", "period": "last_month"},
                {"metric": "physical_activity", "change": "+22%", "period": "last_month"},
                {"metric": "sleep_quality", "change": "+8%", "period": "last_month"}
            ],
            "challenge_areas": [
                {"area": "weekend_consistency", "improvement_suggestion": "Plan weekend activities in advance"},
                {"area": "weather_dependency", "improvement_suggestion": "Add indoor activity alternatives"}
            ]
        },
        "motivation_system": {
            "individual_rewards": [
                {"member": "Emma", "earned": "Choice of weekend activity", "for": "15-day nutrition streak"},
                {"member": "Alex", "earned": "Extra 30 min screen time", "for": "Completing fitness week"}
            ],
            "family_rewards": [
                {"earned": "Family movie night", "for": "Everyone meeting weekly nutrition goal"},
                {"pending": "Weekend camping trip", "requirement": "Complete 4-week fitness challenge"}
            ],
            "celebration_milestones": [
                {"milestone": "1 month of consistent goals", "celebration": "Family dinner at favorite restaurant"},
                {"milestone": "3 months of progress", "celebration": "Family vacation planning session"},
                {"milestone": "6 months of success", "celebration": "Special family adventure day"}
            ]
        }
    }

@api_router.post("/family/goals/{goal_id}/update-progress")
async def update_family_goal_progress(goal_id: str, progress_data: dict):
    """Update progress for family goals"""
    return {
        "goal_id": goal_id,
        "updated": True,
        "new_progress": progress_data.get("progress", 0),
        "member": progress_data.get("member", "unknown"),
        "streak_updated": True,
        "family_progress_recalculated": True,
        "milestone_check": {
            "milestone_reached": progress_data.get("progress", 0) > 80,
            "reward_unlocked": "Family celebration dinner" if progress_data.get("progress", 0) > 80 else None
        },
        "encouragement_message": "Great job staying committed to your family's health goals!",
        "next_milestone": "Keep it up! You're only 5% away from your next reward."
    }

@api_router.get("/family/multi-profile-management/{family_id}")
async def get_multi_profile_management(family_id: str):
    """Advanced multi-profile management system"""
    return {
        "family_id": family_id,
        "profile_overview": {
            "total_profiles": 4,
            "completion_status": {
                "Sarah": {"completion": 95, "status": "complete", "last_updated": "2024-01-16"},
                "John": {"completion": 88, "status": "complete", "last_updated": "2024-01-15"},
                "Emma": {"completion": 92, "status": "complete", "last_updated": "2024-01-17"},
                "Alex": {"completion": 85, "status": "complete", "last_updated": "2024-01-14"}
            },
            "data_synchronization": {
                "last_sync": "2024-01-17 7:00 AM",
                "sync_status": "up_to_date",
                "conflicts_resolved": 0,
                "pending_updates": []
            }
        },
        "member_profiles": [
            {
                "member": "Sarah",
                "role": "Primary Caregiver",
                "age": 38,
                "health_summary": {
                    "current_conditions": ["Pregnancy - 2nd trimester"],
                    "allergies": ["none"],
                    "medications": ["Prenatal vitamins"],
                    "recent_vitals": {"bp": "118/75", "weight": "142 lbs", "heart_rate": "72 bpm"},
                    "health_goals": ["Healthy pregnancy weight gain", "Regular prenatal care", "Stress management"]
                },
                "dietary_preferences": {
                    "restrictions": ["none"],
                    "preferences": ["organic_when_possible", "minimal_processed_foods"],
                    "cultural_dietary": ["Mediterranean_influenced"]
                },
                "activity_level": "moderately_active",
                "responsibilities": ["medication_management", "appointment_scheduling", "meal_planning"]
            },
            {
                "member": "John",
                "role": "Secondary Caregiver",
                "age": 40,
                "health_summary": {
                    "current_conditions": ["Mild hypertension"],
                    "allergies": ["environmental_dust"],
                    "medications": ["Blood pressure medication"],
                    "recent_vitals": {"bp": "132/82", "weight": "185 lbs", "heart_rate": "68 bpm"},
                    "health_goals": ["Blood pressure management", "Weight maintenance", "Regular exercise"]
                },
                "dietary_preferences": {
                    "restrictions": ["low_sodium"],
                    "preferences": ["whole_grains", "lean_proteins"],
                    "cultural_dietary": ["American_traditional"]
                },
                "activity_level": "lightly_active",
                "responsibilities": ["transportation", "emergency_backup", "weekend_meal_prep"]
            },
            {
                "member": "Emma",
                "role": "Dependent - Adolescent", 
                "age": 12,
                "health_summary": {
                    "current_conditions": ["Seasonal allergies"],
                    "allergies": ["tree_nuts_severe", "pollen"],
                    "medications": ["EpiPen", "Allergy medication as needed"],
                    "recent_vitals": {"height": "5'2\"", "weight": "105 lbs", "growth_percentile": "60th"},
                    "health_goals": ["Allergy management", "Healthy growth", "Physical fitness"]
                },
                "dietary_preferences": {
                    "restrictions": ["tree_nuts", "avoids_processed_snacks"],
                    "preferences": ["fruits", "yogurt", "homemade_baked_goods"],
                    "cultural_dietary": ["family_style_meals"]
                },
                "activity_level": "very_active",
                "school_coordination": {
                    "school_nurse_informed": True,
                    "emergency_action_plan": "on_file",
                    "lunch_modifications": "nut_free_table"
                }
            },
            {
                "member": "Alex",
                "role": "Dependent - Child",
                "age": 8,
                "health_summary": {
                    "current_conditions": ["none"],
                    "allergies": ["none_known"],
                    "medications": ["none_regular"],
                    "recent_vitals": {"height": "4'8\"", "weight": "85 lbs", "growth_percentile": "75th"},
                    "health_goals": ["Healthy growth", "Develop good eating habits", "Stay active"],
                    "dietary_considerations": ["lactose_intolerant"]
                },
                "dietary_preferences": {
                    "restrictions": ["dairy_limited"],
                    "preferences": ["chicken", "pasta", "apples", "rice"],
                    "challenges": ["picky_eater", "limited_vegetable_acceptance"]
                },
                "activity_level": "very_active",
                "school_coordination": {
                    "lunch_modifications": "dairy_free_options",
                    "snack_preferences": "nut_free_crackers_fruit"
                }
            }
        ],
        "coordination_tools": {
            "shared_calendar": {
                "medical_appointments": 3,
                "medication_reminders": 5,
                "meal_planning_sessions": 2,
                "family_activities": 8
            },
            "communication_system": {
                "family_chat_active": True,
                "provider_messaging": True,
                "school_communication": True,
                "emergency_notifications": True
            },
            "data_sharing": {
                "with_healthcare_providers": ["with_consent", "secure_portal"],
                "with_schools": ["emergency_info_only", "updated_automatically"],
                "with_family_members": ["age_appropriate_access"]
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

# ===== PHASE 6: GUEST GOAL MANAGEMENT APIS =====

class GuestGoal(BaseModel):
    id: int
    title: str
    category: str
    target: int
    unit: str
    current: int = 0
    timeframe: str = "daily"
    createdAt: str
    lastUpdated: str

class GuestGoalSession(BaseModel):
    session_id: str
    goals: List[GuestGoal] = []
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime

@api_router.post("/guest/goals/{session_id}")
async def sync_guest_goals(session_id: str, goal_data: dict):
    """Sync guest goals with backend for session persistence"""
    try:
        goals_list = goal_data.get('goals', [])
        
        # Store in temporary collection with expiration
        goal_session = {
            "session_id": session_id,
            "goals": goals_list,
            "last_updated": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        }
        
        # Update or insert goal session
        await db.guest_goal_sessions.update_one(
            {"session_id": session_id},
            {"$set": goal_session},
            upsert=True
        )
        
        # Clean up expired sessions
        await db.guest_goal_sessions.delete_many({
            "expires_at": {"$lt": datetime.utcnow()}
        })
        
        return {
            "success": True,
            "session_id": session_id,
            "goals_synced": len(goals_list),
            "expires_at": goal_session["expires_at"].isoformat()
        }
    except Exception as e:
        logger.error(f"Goal sync error: {e}")
        return {"success": False, "error": "Failed to sync goals"}

@api_router.get("/guest/goals/{session_id}")
async def get_guest_goals(session_id: str):
    """Retrieve guest goals for a session"""
    try:
        goal_session = await db.guest_goal_sessions.find_one({
            "session_id": session_id,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        if not goal_session:
            return {
                "success": True,
                "session_id": session_id,
                "goals": [],
                "message": "No goals found for this session"
            }
        
        return {
            "success": True,
            "session_id": session_id,
            "goals": goal_session.get("goals", []),
            "last_updated": goal_session.get("last_updated").isoformat(),
            "expires_at": goal_session.get("expires_at").isoformat()
        }
    except Exception as e:
        logger.error(f"Goal retrieval error: {e}")
        return {"success": False, "error": "Failed to retrieve goals"}

@api_router.post("/guest/goals/{session_id}/progress")
async def update_guest_goal_progress(session_id: str, progress_data: dict):
    """Update progress for a specific goal"""
    try:
        goal_id = progress_data.get('goal_id')
        new_current = progress_data.get('current', 0)
        
        # Update specific goal progress
        result = await db.guest_goal_sessions.update_one(
            {
                "session_id": session_id,
                "expires_at": {"$gt": datetime.utcnow()},
                "goals.id": goal_id
            },
            {
                "$set": {
                    "goals.$.current": new_current,
                    "goals.$.lastUpdated": datetime.utcnow().isoformat(),
                    "last_updated": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            return {
                "success": True,
                "goal_id": goal_id,
                "new_current": new_current,
                "message": "Progress updated successfully"
            }
        else:
            return {"success": False, "error": "Goal not found or session expired"}
            
    except Exception as e:
        logger.error(f"Goal progress update error: {e}")
        return {"success": False, "error": "Failed to update progress"}

@api_router.get("/guest/goals/{session_id}/analytics")
async def get_guest_goal_analytics(session_id: str):
    """Get goal analytics and insights for guest session"""
    try:
        goal_session = await db.guest_goal_sessions.find_one({
            "session_id": session_id,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        if not goal_session:
            return {"success": False, "error": "Session not found or expired"}
        
        goals = goal_session.get("goals", [])
        
        # Calculate analytics
        total_goals = len(goals)
        completed_goals = len([g for g in goals if g.get('current', 0) >= g.get('target', 1)])
        completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0
        
        # Category breakdown
        category_stats = {}
        for goal in goals:
            category = goal.get('category', 'other')
            if category not in category_stats:
                category_stats[category] = {'total': 0, 'completed': 0}
            category_stats[category]['total'] += 1
            if goal.get('current', 0) >= goal.get('target', 1):
                category_stats[category]['completed'] += 1
        
        # Generate insights
        insights = []
        if completion_rate >= 80:
            insights.append("Excellent progress! You're crushing your goals today.")
        elif completion_rate >= 50:
            insights.append("Great work! You're more than halfway to your daily goals.")
        elif completion_rate >= 25:
            insights.append("Good start! Keep going to reach more of your goals.")
        else:
            insights.append("Every step counts! Start with one small goal to build momentum.")
        
        # Add category-specific insights
        for category, stats in category_stats.items():
            if stats['completed'] == stats['total'] and stats['total'] > 0:
                insights.append(f"🎉 Perfect {category} goals completion!")
        
        return {
            "success": True,
            "session_id": session_id,
            "analytics": {
                "total_goals": total_goals,
                "completed_goals": completed_goals,
                "completion_rate": round(completion_rate, 1),
                "category_breakdown": category_stats,
                "session_duration": calculate_session_duration(goal_session.get("last_updated")),
                "insights": insights,
                "motivational_message": get_motivational_message(completion_rate),
                "next_actions": get_next_action_suggestions(goals)
            }
        }
    except Exception as e:
        logger.error(f"Goal analytics error: {e}")
        return {"success": False, "error": "Failed to generate analytics"}

def calculate_session_duration(last_updated):
    """Calculate session duration"""
    if not last_updated:
        return "0 minutes"
    
    duration = datetime.utcnow() - last_updated
    minutes = int(duration.total_seconds() / 60)
    
    if minutes < 60:
        return f"{minutes} minutes"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m"

def get_motivational_message(completion_rate):
    """Get motivational message based on completion rate"""
    if completion_rate >= 100:
        return "🎉 Amazing! You've completed all your goals for today!"
    elif completion_rate >= 75:
        return "🌟 You're almost there! Just a few more goals to go!"
    elif completion_rate >= 50:
        return "💪 Great momentum! Keep pushing towards your goals!"
    elif completion_rate >= 25:
        return "🚀 Good progress! Every small step counts!"
    else:
        return "🌱 Start with one goal - you've got this!"

def get_next_action_suggestions(goals):
    """Get actionable next step suggestions"""
    suggestions = []
    
    incomplete_goals = [g for g in goals if g.get('current', 0) < g.get('target', 1)]
    
    if not incomplete_goals:
        suggestions.append("All goals completed! Consider setting a bonus goal.")
        return suggestions
    
    # Find easiest goal to complete
    easiest_goal = min(incomplete_goals, 
                      key=lambda g: g.get('target', 1) - g.get('current', 0))
    
    remaining = easiest_goal.get('target', 1) - easiest_goal.get('current', 0)
    if remaining == 1:
        suggestions.append(f"Quick win: Complete '{easiest_goal.get('title', 'Unknown')}' - just 1 more {easiest_goal.get('unit', 'step')}!")
    else:
        suggestions.append(f"Focus on '{easiest_goal.get('title', 'Unknown')}' - {remaining} {easiest_goal.get('unit', 'steps')} to go!")
    
    # Category-specific suggestions
    nutrition_goals = [g for g in incomplete_goals if g.get('category') == 'nutrition']
    if nutrition_goals:
        suggestions.append("💡 Add vegetables to your next meal for nutrition goal progress!")
    
    hydration_goals = [g for g in incomplete_goals if g.get('category') == 'hydration']
    if hydration_goals:
        suggestions.append("💧 Keep a water bottle nearby to stay on track!")
    
    return suggestions[:3]  # Limit to 3 suggestions

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# PHASE 7: DATA EXPORT ENDPOINTS
# ========================================

@api_router.get("/patient/export/{user_id}")
async def export_patient_data(user_id: str, format: str = "json"):
    """Export comprehensive patient data"""
    try:
        # Get patient profile
        profile = await db.patient_profiles.find_one({"user_id": user_id})
        if not profile:
            raise HTTPException(status_code=404, detail="Patient profile not found")
        
        # Collect all patient data
        export_data = {
            "export_info": {
                "user_id": user_id,
                "role": "patient",
                "exported_at": datetime.utcnow().isoformat(),
                "format": format
            },
            "profile": {
                "user_id": profile.get("user_id"),
                "basic_info": profile.get("basic_info", {}),
                "physical_metrics": profile.get("physical_metrics", {}),
                "activity_profile": profile.get("activity_profile", {}),
                "health_history": profile.get("health_history", {}),
                "dietary_profile": profile.get("dietary_profile", {}),
                "goals_preferences": profile.get("goals_preferences", {}),
                "profile_completion": profile.get("profile_completion", 0)
            },
            "health_data": {
                "nutrition_summary": {
                    "daily_calories": 1850,
                    "protein": 120,
                    "carbs": 180,
                    "fats": 65,
                    "fiber": 25,
                    "water": 8
                },
                "health_metrics": {
                    "weight": 68.5,
                    "bmi": 22.1,
                    "body_fat": 15.2,
                    "blood_pressure": "118/76",
                    "heart_rate": 68
                },
                "goals": [
                    {"id": "weight_goal", "title": "Maintain healthy weight", "target": 68, "current": 68.5, "unit": "kg"},
                    {"id": "protein_goal", "title": "Daily protein intake", "target": 120, "current": 95, "unit": "g"},
                    {"id": "hydration_goal", "title": "Daily water intake", "target": 8, "current": 6, "unit": "glasses"}
                ]
            },
            "food_logs": [
                {
                    "date": "2024-07-15",
                    "meals": {
                        "breakfast": [{"food": "Oatmeal with berries", "calories": 280, "protein": 8}],
                        "lunch": [{"food": "Grilled chicken salad", "calories": 420, "protein": 35}],
                        "dinner": [{"food": "Salmon with quinoa", "calories": 580, "protein": 40}],
                        "snacks": [{"food": "Greek yogurt", "calories": 150, "protein": 15}]
                    },
                    "total_calories": 1430,
                    "total_protein": 98
                }
            ],
            "ai_insights": [
                "Your protein intake is consistently good, averaging 98g daily",
                "Consider increasing vegetable variety for better micronutrient profile",
                "Your meal timing is optimal for metabolism"
            ]
        }
        
        return export_data
        
    except Exception as e:
        logger.error(f"Error exporting patient data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@api_router.get("/provider/export/{user_id}")
async def export_provider_data(user_id: str, format: str = "json"):
    """Export comprehensive provider data"""
    try:
        # Get provider profile
        profile = await db.provider_profiles.find_one({"user_id": user_id})
        if not profile:
            raise HTTPException(status_code=404, detail="Provider profile not found")
        
        export_data = {
            "export_info": {
                "user_id": user_id,
                "role": "provider",
                "exported_at": datetime.utcnow().isoformat(),
                "format": format
            },
            "profile": {
                "user_id": profile.get("user_id"),
                "professional_identity": profile.get("professional_identity", {}),
                "credentials": profile.get("credentials", {}),
                "practice_info": profile.get("practice_info", {}),
                "preferences": profile.get("preferences", {}),
                "verification_status": profile.get("verification_status", "PENDING"),
                "profile_completion": profile.get("profile_completion", 0)
            },
            "practice_data": {
                "patient_overview": {
                    "total_patients": 47,
                    "active_patients": 42,
                    "patients_seen_today": 8,
                    "avg_patient_satisfaction": 4.7
                },
                "clinical_analytics": {
                    "successful_outcomes": 89.2,
                    "patient_adherence_rate": 76.3,
                    "intervention_effectiveness": 84.1
                },
                "recent_activities": [
                    {"date": "2024-07-15", "activity": "Patient consultation - John D.", "outcome": "Treatment plan updated"},
                    {"date": "2024-07-15", "activity": "Nutrition review - Sarah M.", "outcome": "Goals achieved"},
                    {"date": "2024-07-14", "activity": "Follow-up - Maria L.", "outcome": "Excellent progress"}
                ]
            },
            "professional_insights": [
                "85% of your patients show improvement in nutritional adherence",
                "Your personalized meal plans have 92% satisfaction rate",
                "Consider offering group nutrition sessions for better engagement"
            ]
        }
        
        return export_data
        
    except Exception as e:
        logger.error(f"Error exporting provider data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@api_router.get("/family/export/{family_id}")
async def export_family_data(family_id: str, format: str = "json"):
    """Export comprehensive family data"""
    try:
        # Get family profile
        profile = await db.family_profiles.find_one({"user_id": family_id})
        if not profile:
            raise HTTPException(status_code=404, detail="Family profile not found")
        
        export_data = {
            "export_info": {
                "family_id": family_id,
                "role": "family",
                "exported_at": datetime.utcnow().isoformat(),
                "format": format
            },
            "profile": {
                "user_id": profile.get("user_id"),
                "family_structure": profile.get("family_structure", {}),
                "family_members": profile.get("family_members", []),
                "household_management": profile.get("household_management", {}),
                "care_coordination": profile.get("care_coordination", {}),
                "profile_completion": profile.get("profile_completion", 0)
            },
            "family_health_data": {
                "member_health_summary": [
                    {"name": "Sarah (Mom)", "age": 35, "health_status": "Excellent", "goals_met": "80%"},
                    {"name": "John (Dad)", "age": 38, "health_status": "Good", "goals_met": "75%"},
                    {"name": "Emma (Daughter)", "age": 8, "health_status": "Excellent", "goals_met": "95%"},
                    {"name": "Max (Son)", "age": 12, "health_status": "Good", "goals_met": "70%"}
                ],
                "family_goals": [
                    {"goal": "Family fitness challenge", "progress": "85%", "participants": 4},
                    {"goal": "Healthy meal prep Sundays", "progress": "90%", "participants": 4},
                    {"goal": "Reduce screen time", "progress": "60%", "participants": 2}
                ]
            },
            "meal_planning": {
                "weekly_meals": [
                    {"day": "Monday", "breakfast": "Overnight oats", "lunch": "Turkey sandwiches", "dinner": "Grilled chicken with vegetables"},
                    {"day": "Tuesday", "breakfast": "Smoothie bowls", "lunch": "Quinoa salad", "dinner": "Fish tacos"},
                    {"day": "Wednesday", "breakfast": "Egg scramble", "lunch": "Soup and salad", "dinner": "Pasta with marinara"}
                ],
                "dietary_accommodations": ["Gluten-free options for Emma", "Low-sodium for John"],
                "budget_tracking": {"weekly_budget": 150, "spent": 142, "savings": 8}
            },
            "care_coordination": {
                "medical_appointments": [
                    {"member": "Emma", "date": "2024-07-20", "type": "Pediatric checkup", "provider": "Dr. Smith"},
                    {"member": "John", "date": "2024-07-18", "type": "Cardiology follow-up", "provider": "Dr. Johnson"}
                ],
                "emergency_contacts": profile.get("care_coordination", {}).get("emergency_contacts", []),
                "healthcare_providers": profile.get("care_coordination", {}).get("healthcare_providers", [])
            }
        }
        
        return export_data
        
    except Exception as e:
        logger.error(f"Error exporting family data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@api_router.get("/guest/export/{session_id}")
async def export_guest_data(session_id: str, format: str = "json"):
    """Export guest session data"""
    try:
        # Get guest profile
        profile = await db.guest_profiles.find_one({"session_id": session_id})
        if not profile:
            raise HTTPException(status_code=404, detail="Guest session not found or expired")
        
        # Check if session is still valid
        if profile.get("expires_at") and datetime.fromisoformat(profile["expires_at"]) < datetime.utcnow():
            raise HTTPException(status_code=410, detail="Session expired")
        
        export_data = {
            "export_info": {
                "session_id": session_id,
                "role": "guest",
                "exported_at": datetime.utcnow().isoformat(),
                "format": format,
                "session_expires_at": profile.get("expires_at")
            },
            "profile": {
                "session_id": profile.get("session_id"),
                "demographics": profile.get("demographics", {}),
                "goals": profile.get("goals", {}),
                "created_at": profile.get("created_at"),
                "expires_at": profile.get("expires_at")
            },
            "session_data": {
                "todays_entries": {
                    "foods_logged": [
                        {"food": "Apple", "calories": 80, "time": "09:30"},
                        {"food": "Sandwich", "calories": 350, "time": "12:15"},
                        {"food": "Water (500ml)", "calories": 0, "time": "14:00"}
                    ],
                    "total_calories": 430,
                    "meals_logged": 2
                },
                "nutrition_summary": {
                    "daily_goal": 2000,
                    "consumed": 430,
                    "remaining": 1570,
                    "protein": 15,
                    "carbs": 85,
                    "fats": 12
                },
                "simple_goals": [
                    {"goal": "Drink 8 glasses of water", "target": 8, "current": 3, "unit": "glasses"},
                    {"goal": "Eat 5 servings of fruits/vegetables", "target": 5, "current": 1, "unit": "servings"},
                    {"goal": "Take daily vitamins", "target": 1, "current": 1, "unit": "dose"}
                ]
            },
            "insights": [
                "You're 21% towards your daily calorie goal",
                "Great start on hydration - keep it up!",
                "Consider adding more protein to your meals"
            ],
            "upgrade_benefits": {
                "features_available_with_account": [
                    "Permanent data storage",
                    "Advanced analytics",
                    "Meal planning tools",
                    "Progress tracking over time",
                    "Personalized recommendations"
                ],
                "current_limitations": [
                    "24-hour session limit",
                    "Basic goal tracking only",
                    "Limited food database"
                ]
            }
        }
        
        return export_data
        
    except Exception as e:
        logger.error(f"Error exporting guest data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
