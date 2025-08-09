import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import RoleSelection from "./components/RoleSelection";
import PatientDashboard from "./components/PatientDashboard";
import ProviderDashboard from "./components/ProviderDashboard";
import FamilyDashboard from "./components/FamilyDashboard";
import GuestDashboard from "./components/GuestDashboard";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RoleSelection />} />
          <Route path="/patient-dashboard" element={<PatientDashboard />} />
          <Route path="/provider-dashboard" element={<ProviderDashboard />} />
          <Route path="/family-dashboard" element={<FamilyDashboard />} />
          <Route path="/guest-dashboard" element={<GuestDashboard />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;