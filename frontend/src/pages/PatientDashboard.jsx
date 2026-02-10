import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

const PatientDashboard = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [diagnoses, setDiagnoses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) {
      navigate('/login')
      return
    }
    loadDiagnoses()
  }, [user, navigate])

  const loadDiagnoses = async () => {
    try {
      const response = await api.get('/dermatology/diagnoses')
      setDiagnoses(response.data.slice(0, 5)) // Show last 5
    } catch (error) {
      console.error('Failed to load diagnoses:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">
              Dermatology AI Assistant
            </h1>
            <div className="flex items-center gap-4">
              <span className="text-gray-600">Welcome, {user?.full_name}</span>
              <button onClick={handleLogout} className="btn-secondary">
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <button
            onClick={() => navigate('/analyze')}
            className="card hover:shadow-lg transition-shadow cursor-pointer border-2 border-primary-500"
          >
            <div className="text-center">
              <div className="text-4xl mb-4">🔬</div>
              <h3 className="text-xl font-semibold mb-2">New Analysis</h3>
              <p className="text-gray-600">Upload image for AI diagnosis</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/history')}
            className="card hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div className="text-center">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2">View History</h3>
              <p className="text-gray-600">See past diagnoses</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/chat')}
            className="card hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div className="text-center">
              <div className="text-4xl mb-4">💬</div>
              <h3 className="text-xl font-semibold mb-2">AI Chat</h3>
              <p className="text-gray-600">Ask questions</p>
            </div>
          </button>
        </div>

        {/* Recent Diagnoses */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Recent Diagnoses</h2>
          
          {loading ? (
            <p className="text-gray-600">Loading...</p>
          ) : diagnoses.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-600 mb-4">No diagnoses yet</p>
              <button
                onClick={() => navigate('/analyze')}
                className="btn-primary"
              >
                Start Your First Analysis
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {diagnoses.map((diagnosis) => (
                <div
                  key={diagnosis.id}
                  className="border border-gray-200 rounded-lg p-4 hover:border-primary-500 transition-colors"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-lg">
                        {diagnosis.primary_prediction}
                      </h3>
                      <p className="text-sm text-gray-600">
                        Confidence: {(diagnosis.confidence_score * 100).toFixed(1)}%
                      </p>
                      <p className="text-sm text-gray-600">
                        Risk Level: <span className={`font-semibold ${
                          diagnosis.risk_level === 'high' ? 'text-red-600' :
                          diagnosis.risk_level === 'medium' ? 'text-yellow-600' :
                          'text-green-600'
                        }`}>{diagnosis.risk_level}</span>
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-500">
                        {new Date(diagnosis.created_at).toLocaleDateString()}
                      </p>
                      <span className={`text-xs px-2 py-1 rounded ${
                        diagnosis.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                        diagnosis.status === 'rejected' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {diagnosis.status.replace('_', ' ')}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Medical Disclaimer */}
        <div className="mt-8 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
          <p className="text-sm text-yellow-800">
            <strong>Medical Disclaimer:</strong> This AI system is designed to assist healthcare 
            professionals, not replace them. All diagnoses should be reviewed by qualified 
            dermatologists before making clinical decisions.
          </p>
        </div>
      </main>
    </div>
  )
}

export default PatientDashboard
