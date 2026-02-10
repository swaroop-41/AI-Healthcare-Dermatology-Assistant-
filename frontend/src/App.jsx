import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import PatientDashboard from './pages/PatientDashboard'
import AnalysisPage from './pages/AnalysisPage'
import HistoryPage from './pages/HistoryPage'
import AdminDashboard from './pages/AdminDashboard'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/dashboard" element={<PatientDashboard />} />
            <Route path="/analyze" element={<AnalysisPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
