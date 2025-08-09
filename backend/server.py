from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime


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

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Health & Nutrition Platform API"}

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
        "daily_calories": 1847,
        "foods_logged": 12,
        "goals_met": "3/5",
        "health_score": "87%",
        "recent_activities": [
            {"type": "food_log", "description": "Logged breakfast: Oatmeal with berries"},
            {"type": "goal", "description": "Completed water intake goal"},
            {"type": "recommendation", "description": "New meal plan recommendation available"}
        ]
    }

# Provider-specific endpoints
@api_router.get("/provider/dashboard/{user_id}")
async def get_provider_dashboard(user_id: str):
    return {
        "user_id": user_id,
        "active_patients": 247,
        "prescriptions": 156,
        "analytics_score": "94%",
        "consultations": 12,
        "recent_updates": [
            {"type": "assessment", "description": "Patient John D. completed nutrition assessment"},
            {"type": "prescription", "description": "New prescription request from Sarah M."},
            {"type": "report", "description": "Weekly report ready for review"}
        ]
    }

# Family-specific endpoints
@api_router.get("/family/dashboard/{user_id}")
async def get_family_dashboard(user_id: str):
    return {
        "user_id": user_id,
        "family_members": 4,
        "health_alerts": 2,
        "appointments": 3,
        "coverage": "100%",
        "family_updates": [
            {"type": "achievement", "description": "Emma completed her daily nutrition goals"},
            {"type": "reminder", "description": "Reminder: Alex's doctor appointment tomorrow"},
            {"type": "report", "description": "Weekly family health report available"}
        ]
    }

# Guest-specific endpoints
@api_router.get("/guest/dashboard")
async def get_guest_dashboard():
    return {
        "quick_logs": 5,
        "session_time": "15m",
        "features_used": 3,
        "experience": "Good",
        "message": "Guest session active - data will not be permanently saved"
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
