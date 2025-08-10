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

// Provider navigation pages
import ProviderPatients from "./components/ProviderPatients";
import ProviderTools from "./components/ProviderTools";
import ProviderAnalytics from "./components/ProviderAnalytics";

// Guest navigation pages
import GuestFoodLog from "./components/GuestFoodLog";
import GuestNutritionTips from "./components/GuestNutritionTips";

// Family navigation pages
import FamilyMembers from "./components/FamilyMembers";
import FamilyMeals from "./components/FamilyMeals";

function App() {
  return (
    &lt;div className="App"&gt;
      &lt;RoleProvider&gt;
        &lt;BrowserRouter&gt;
          &lt;Routes&gt;
            &lt;Route path="/" element={&lt;RoleSelection /&gt;} /&gt;
            
            {/* Dashboard Routes */}
            &lt;Route path="/patient-dashboard" element={&lt;PatientDashboard /&gt;} /&gt;
            &lt;Route path="/provider-dashboard" element={&lt;ProviderDashboard /&gt;} /&gt;
            &lt;Route path="/family-dashboard" element={&lt;FamilyDashboard /&gt;} /&gt;
            &lt;Route path="/guest-dashboard" element={&lt;GuestDashboard /&gt;} /&gt;
            
            {/* Profile Routes */}
            &lt;Route path="/patient-profile" element={&lt;PatientProfileWizard /&gt;} /&gt;
            &lt;Route path="/provider-profile" element={&lt;ProviderProfileWizard /&gt;} /&gt;
            &lt;Route path="/family-profile" element={&lt;FamilyProfileWizard /&gt;} /&gt;
            &lt;Route path="/guest-setup" element={&lt;GuestProfileSetup /&gt;} /&gt;
            
            {/* Patient Navigation Routes */}
            &lt;Route path="/patient-food-log" element={&lt;PatientFoodLog /&gt;} /&gt;
            &lt;Route path="/patient-metrics" element={&lt;PatientHealthMetrics /&gt;} /&gt;
            &lt;Route path="/patient-goals" element={&lt;PatientGoals /&gt;} /&gt;
            &lt;Route path="/patient-analytics" element={&lt;PatientAnalytics /&gt;} /&gt;
            
            {/* Provider Navigation Routes */}
            &lt;Route path="/provider-patients" element={&lt;ProviderPatients /&gt;} /&gt;
            &lt;Route path="/provider-tools" element={&lt;ProviderTools /&gt;} /&gt;
            &lt;Route path="/provider-analytics" element={&lt;ProviderAnalytics /&gt;} /&gt;
            
            {/* Family Navigation Routes */}
            &lt;Route path="/family-members" element={&lt;FamilyMembers /&gt;} /&gt;
            &lt;Route path="/family-meals" element={&lt;FamilyMeals /&gt;} /&gt;
            
            {/* Guest Navigation Routes */}
            &lt;Route path="/guest-food-log" element={&lt;GuestFoodLog /&gt;} /&gt;
            &lt;Route path="/guest-tips" element={&lt;GuestNutritionTips /&gt;} /&gt;
          &lt;/Routes&gt;
        &lt;/BrowserRouter&gt;
      &lt;/RoleProvider&gt;
    &lt;/div&gt;
  );
}

export default App;