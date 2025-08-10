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

// Provider navigation pages
import ProviderPatients from "./components/ProviderPatients";
import ProviderTools from "./components/ProviderTools";
import ProviderAnalytics from "./components/ProviderAnalytics";

// Guest navigation pages
import GuestFoodLog from "./components/GuestFoodLog";
import GuestNutritionTips from "./components/GuestNutritionTips";

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
            
            {/* Provider Navigation Routes */}
            <Route path="/provider-patients" element={<ProviderPatients />} />
            <Route path="/provider-tools" element={<ProviderTools />} />
            <Route path="/provider-analytics" element={<ProviderAnalytics />} />
            
            {/* Guest Navigation Routes */}
            <Route path="/guest-food-log" element={<GuestFoodLog />} />
            <Route path="/guest-tips" element={<GuestNutritionTips />} />
          </Routes>
        </BrowserRouter>
      </RoleProvider>
    </div>
  );
}

export default App;