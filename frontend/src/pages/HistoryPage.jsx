import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const HistoryPage = () => {
  const navigate = useNavigate()
  const [diagnoses, setDiagnoses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDiagnoses()
  }, [])

  const loadDiagnoses = async () => {
    try {
      const response = await api.get('/dermatology/diagnoses')
      setDiagnoses(response.data)
    } catch (error) {
      console.error('Failed to load diagnoses:', error)
    } finally {
      setLoading(false)
    }
  }

  const downloadReport = async (diagnosisId) => {
    try {
      const response = await api.get(`/reports/generate/${diagnosisId}`, {
        responseType: 'blob'
      })
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `report_${diagnosisId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Failed to download report:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Diagnosis History</h1>
            <button onClick={() => navigate('/dashboard')} className="btn-secondary">
              Back to Dashboard
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card">
          {loading ? (
            <p className="text-gray-600">Loading...</p>
          ) : diagnoses.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-600 mb-4">No diagnoses found</p>
              <button onClick={() => navigate('/analyze')} className="btn-primary">
                Start Your First Analysis
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              {diagnoses.map((diagnosis) => (
                <div
                  key={diagnosis.id}
                  className="border border-gray-200 rounded-lg p-6"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-xl font-semibold">{diagnosis.primary_prediction}</h3>
                      <p className="text-gray-600">
                        {new Date(diagnosis.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      diagnosis.risk_level === 'high' ? 'bg-red-100 text-red-800' :
                      diagnosis.risk_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {diagnosis.risk_level} risk
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600">Confidence</p>
                      <p className="font-semibold">
                        {(diagnosis.confidence_score * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Status</p>
                      <p className="font-semibold capitalize">
                        {diagnosis.status.replace('_', ' ')}
                      </p>
                    </div>
                  </div>

                  {diagnosis.recommendation && (
                    <div className="bg-blue-50 p-3 rounded-lg mb-4">
                      <p className="text-sm text-blue-900">
                        <strong>Recommendation:</strong> {diagnosis.recommendation}
                      </p>
                    </div>
                  )}

                  <button
                    onClick={() => downloadReport(diagnosis.id)}
                    className="btn-primary text-sm"
                  >
                    Download PDF Report
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default HistoryPage
