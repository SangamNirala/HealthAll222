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

function App() {
  return (
    <div className="App">
      <RoleProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<RoleSelection />} />
            <Route path="/patient-dashboard" element={<PatientDashboard />} />
            <Route path="/provider-dashboard" element={<ProviderDashboard />} />
            <Route path="/family-dashboard" element={<FamilyDashboard />} />
            <Route path="/guest-dashboard" element={<GuestDashboard />} />
            <Route path="/patient-profile" element={<PatientProfileWizard />} />
            <Route path="/provider-profile" element={<ProviderProfileWizard />} />
            <Route path="/family-profile" element={<FamilyProfileWizard />} />
            <Route path="/guest-setup" element={<GuestProfileSetup />} />
          </Routes>
        </BrowserRouter>
      </RoleProvider>
    </div>
  );
}

export default App;