import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { RoleProvider } from "./context/RoleContext";
import RoleSelection from "./components/RoleSelection";
import PatientDashboard from "./components/PatientDashboard";
import ProviderDashboard from "./components/ProviderDashboard";
import FamilyDashboard from "./components/FamilyDashboard";
import GuestDashboard from "./components/GuestDashboard";
import PatientProfileWizard from "./components/profiles/PatientProfileWizard";
import ProviderProfileWizard from "./components/profiles/ProviderProfileWizard";
import FamilyProfileWizard from "./components/profiles/FamilyProfileWizard";
import GuestProfileSetup from "./components/profiles/GuestProfileSetup";

// Patient navigation pages
import PatientFoodLog from "./components/PatientFoodLog";
import PatientHealthMetrics from "./components/PatientHealthMetrics";
import PatientGoals from "./components/PatientGoals";
import PatientAnalytics from "./components/PatientAnalytics";
import PatientMedicationReminder from "./components/PatientMedicationReminder";
import PatientHealthTimeline from "./components/PatientHealthTimeline";
import EnhancedMedicationManager from "./components/EnhancedMedicationManager";
import DrugInteractionWarnings from "./components/DrugInteractionWarnings";

// Analytics components
import PersonalInsights from "./components/analytics/PersonalInsights";

// Goals components  
import AdvancedGoalTracking from "./components/goals/AdvancedGoalTracking";

// Provider navigation pages
import ProviderPatients from "./components/ProviderPatients";
import ProviderTools from "./components/ProviderTools";
import ProviderAnalytics from "./components/ProviderAnalytics";
import ProviderEducation from "./components/ProviderEducation";
import ProviderMedicationDashboard from "./components/ProviderMedicationDashboard";
import PatientMedicationProvider from "./components/PatientMedicationProvider";
import ClinicalDashboard from "./components/ClinicalDashboard";

// Guest navigation pages
import GuestFoodLog from "./components/GuestFoodLog";
import GuestNutritionTips from "./components/GuestNutritionTips";
import GuestHealthCalculator from "./components/GuestHealthCalculator";
import GuestGoals from "./components/GuestGoals";
import InstantHealthAssessment from "./components/InstantHealthAssessment";
import AIFoodRecognition from "./components/AIFoodRecognition";
import QuickSymptomCheckerPage from "./components/QuickSymptomCheckerPage";

// Family navigation pages
import FamilyMembers from "./components/FamilyMembers";
import FamilyMeals from "./components/FamilyMeals";

// Phase 5: Advanced Family Features
import FamilyCoordination from "./components/FamilyCoordination";
import FamilyCalendar from "./components/FamilyCalendar";
import ChildNutritionEducation from "./components/ChildNutritionEducation";
import CaregiverTools from "./components/CaregiverTools";
import FamilyGoalsCoordination from "./components/FamilyGoalsCoordination";
import MultiProfileManagement from "./components/MultiProfileManagement";

// Patient Management Components
import SmartPatientAssignmentPanel from "./components/patient-management/SmartPatientAssignmentPanel";
import RealTimeProgressDashboard from "./components/patient-management/RealTimeProgressDashboard";
import IntelligentMealPlanGenerator from "./components/patient-management/IntelligentMealPlanGenerator";
import AdvancedAdherenceMonitor from "./components/patient-management/AdvancedAdherenceMonitor";
import AutomatedReportGenerator from "./components/patient-management/AutomatedReportGenerator";
import IntelligentAlertSystem from "./components/patient-management/IntelligentAlertSystem";
import VirtualConsultationCenter from "./components/patient-management/VirtualConsultationCenter";
import PatientEngagementHub from "./components/patient-management/PatientEngagementHub";
import EnhancedPatientManagementSystem from "./components/patient-management/EnhancedPatientManagementSystem";

function App() {
  return (
    <div className="App">
      <RoleProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<RoleSelection />} />
            
            {/* Dashboard Routes */}
            <Route path="/patient-dashboard" element={<PatientDashboard />} />
            <Route path="/provider-dashboard" element={<ProviderDashboard />} />
            <Route path="/family-dashboard" element={<FamilyDashboard />} />
            <Route path="/guest-dashboard" element={<GuestDashboard />} />
            
            {/* Profile Routes */}
            <Route path="/patient-profile" element={<PatientProfileWizard />} />
            <Route path="/provider-profile" element={<ProviderProfileWizard />} />
            <Route path="/family-profile" element={<FamilyProfileWizard />} />
            <Route path="/guest-setup" element={<GuestProfileSetup />} />
            
            {/* Patient Navigation Routes */}
            <Route path="/patient-food-log" element={<PatientFoodLog />} />
            <Route path="/patient-metrics" element={<PatientHealthMetrics />} />
            <Route path="/patient-goals" element={<PatientGoals />} />
            <Route path="/patient-analytics" element={<PatientAnalytics />} />
            <Route path="/patient-medications" element={<PatientMedicationReminder />} />
            <Route path="/enhanced-medications" element={<EnhancedMedicationManager />} />
            <Route path="/drug-interactions" element={<DrugInteractionWarnings />} />
            <Route path="/patient-timeline" element={<PatientHealthTimeline />} />
            <Route path="/personal-insights" element={<PersonalInsights />} />
            <Route path="/advanced-goals" element={<AdvancedGoalTracking />} />
            
            {/* Provider Navigation Routes */}
            <Route path="/provider-patients" element={<ProviderPatients />} />
            <Route path="/provider-tools" element={<ProviderTools />} />
            <Route path="/provider-analytics" element={<ProviderAnalytics />} />
            <Route path="/provider-education" element={<ProviderEducation />} />
            <Route path="/provider-medication-dashboard" element={<ProviderMedicationDashboard />} />
            <Route path="/provider-clinical-dashboard" element={<ClinicalDashboard />} />
            <Route path="/patient-provider-connection" element={<PatientMedicationProvider />} />
            
            {/* Patient Management Routes */}
            <Route path="/smart-patient-assignments" element={<SmartPatientAssignmentPanel />} />
            <Route path="/progress-dashboard" element={<RealTimeProgressDashboard />} />
            <Route path="/intelligent-meal-planning" element={<IntelligentMealPlanGenerator />} />
            <Route path="/adherence-monitor" element={<AdvancedAdherenceMonitor />} />
            <Route path="/report-generator" element={<AutomatedReportGenerator />} />
            <Route path="/alert-system" element={<IntelligentAlertSystem />} />
            <Route path="/virtual-consultation" element={<VirtualConsultationCenter />} />
            <Route path="/patient-engagement" element={<PatientEngagementHub />} />
            <Route path="/enhanced-patient-management" element={<EnhancedPatientManagementSystem />} />
            
            {/* Family Navigation Routes */}
            <Route path="/family-members" element={<FamilyMembers />} />
            <Route path="/family-meals" element={<FamilyMeals />} />
            
            {/* Phase 5: Advanced Family Features Routes */}
            <Route path="/family-coordination" element={<FamilyCoordination />} />
            <Route path="/family-calendar" element={<FamilyCalendar />} />
            <Route path="/child-nutrition-education" element={<ChildNutritionEducation />} />
            <Route path="/caregiver-tools" element={<CaregiverTools />} />
            <Route path="/family-goals" element={<FamilyGoalsCoordination />} />
            <Route path="/multi-profile-management" element={<MultiProfileManagement />} />
            
            {/* Guest Navigation Routes */}
            <Route path="/guest-food-log" element={<GuestFoodLog />} />
            <Route path="/guest-calculator" element={<GuestHealthCalculator />} />
            <Route path="/guest-tips" element={<GuestNutritionTips />} />
            <Route path="/guest-goals" element={<GuestGoals />} />
            <Route path="/instant-health-check" element={<InstantHealthAssessment />} />
            <Route path="/ai-food-scan" element={<AIFoodRecognition />} />
          </Routes>
        </BrowserRouter>
      </RoleProvider>
    </div>
  );
}

export default App;