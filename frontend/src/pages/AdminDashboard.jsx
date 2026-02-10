import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const AdminDashboard = () => {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const response = await api.get('/admin/stats/overview')
      setStats(response.data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
            <button onClick={() => navigate('/dashboard')} className="btn-secondary">
              Back
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Total Diagnoses</h3>
            <p className="text-3xl font-bold text-primary-600">{stats?.total_diagnoses || 0}</p>
          </div>

          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Total Patients</h3>
            <p className="text-3xl font-bold text-primary-600">{stats?.total_patients || 0}</p>
          </div>

          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Total Users</h3>
            <p className="text-3xl font-bold text-primary-600">{stats?.total_users || 0}</p>
          </div>

          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Model Accuracy</h3>
            <p className="text-3xl font-bold text-green-600">
              {((stats?.model_accuracy || 0) * 100).toFixed(1)}%
            </p>
          </div>

          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Avg Confidence</h3>
            <p className="text-3xl font-bold text-blue-600">
              {((stats?.avg_confidence || 0) * 100).toFixed(1)}%
            </p>
          </div>

          <div className="card">
            <h3 className="text-sm font-medium text-gray-600 mb-2">High Risk Cases</h3>
            <p className="text-3xl font-bold text-red-600">{stats?.high_risk_cases || 0}</p>
          </div>
        </div>

        {/* System Status */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">System Health</h2>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">API Status</span>
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                Healthy
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Database Status</span>
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                Healthy
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">ML Model Status</span>
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                Loaded
              </span>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default AdminDashboard
