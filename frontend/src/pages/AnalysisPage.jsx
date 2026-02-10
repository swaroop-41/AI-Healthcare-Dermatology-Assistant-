import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'
import api from '../services/api'

const AnalysisPage = () => {
  const navigate = useNavigate()
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [bodyLocation, setBodyLocation] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxSize: 10485760, // 10MB
    multiple: false,
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0]
      if (file) {
        setSelectedFile(file)
        setPreview(URL.createObjectURL(file))
        setError('')
      }
    }
  })

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image')
      return
    }

    setAnalyzing(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      if (bodyLocation) {
        formData.append('body_location', bodyLocation)
      }

      const response = await api.post('/dermatology/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setAnalyzing(false)
    }
  }

  const handleNewAnalysis = () => {
    setSelectedFile(null)
    setPreview(null)
    setBodyLocation('')
    setResult(null)
    setError('')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">AI Skin Analysis</h1>
            <button onClick={() => navigate('/dashboard')} className="btn-secondary">
              Back to Dashboard
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!result ? (
          <div className="space-y-6">
            {/* Image Upload */}
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Upload Skin Image</h2>
              
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                  isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-400'
                }`}
              >
                <input {...getInputProps()} />
                {preview ? (
                  <div>
                    <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded-lg" />
                    <p className="mt-4 text-sm text-gray-600">Click or drag to change image</p>
                  </div>
                ) : (
                  <div>
                    <div className="text-6xl mb-4">📸</div>
                    <p className="text-lg text-gray-700">
                      {isDragActive ? 'Drop image here' : 'Drag & drop an image, or click to select'}
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      Supported formats: JPEG, PNG (max 10MB)
                    </p>
                  </div>
                )}
              </div>

              {selectedFile && (
                <div className="mt-4">
                  <p className="text-sm text-gray-600">
                    Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                  </p>
                </div>
              )}
            </div>

            {/* Additional Info */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Additional Information</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Body Location (Optional)
                </label>
                <select
                  value={bodyLocation}
                  onChange={(e) => setBodyLocation(e.target.value)}
                  className="input-field"
                >
                  <option value="">Select location</option>
                  <option value="face">Face</option>
                  <option value="neck">Neck</option>
                  <option value="chest">Chest</option>
                  <option value="back">Back</option>
                  <option value="arms">Arms</option>
                  <option value="legs">Legs</option>
                  <option value="hands">Hands</option>
                  <option value="feet">Feet</option>
                </select>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 text-red-600 p-4 rounded-lg">
                {error}
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={!selectedFile || analyzing}
              className="w-full btn-primary disabled:opacity-50"
            >
              {analyzing ? 'Analyzing...' : 'Analyze Image'}
            </button>
          </div>
        ) : (
          /* Results */
          <div className="space-y-6">
            <div className="card">
              <h2 className="text-2xl font-semibold mb-4">Analysis Results</h2>
              
              {/* Primary Diagnosis */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Primary Diagnosis</h3>
                <div className="bg-primary-50 p-4 rounded-lg">
                  <p className="text-2xl font-bold text-primary-700">
                    {result.diagnosis.primary_prediction}
                  </p>
                  <p className="text-gray-600">
                    Confidence: {(result.diagnosis.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              </div>

              {/* ABCDE Scores */}
              {result.clinical_analysis?.abcde_score && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-2">ABCDE Analysis</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-gray-50 p-3 rounded">
                      <p className="text-sm text-gray-600">Asymmetry</p>
                      <p className="text-lg font-semibold">
                        {result.clinical_analysis.abcde_score.asymmetry.toFixed(2)}
                      </p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <p className="text-sm text-gray-600">Border</p>
                      <p className="text-lg font-semibold">
                        {result.clinical_analysis.abcde_score.border.toFixed(2)}
                      </p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <p className="text-sm text-gray-600">Color</p>
                      <p className="text-lg font-semibold">
                        {result.clinical_analysis.abcde_score.color.toFixed(2)}
                      </p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <p className="text-sm text-gray-600">Diameter</p>
                      <p className="text-lg font-semibold">
                        {result.clinical_analysis.abcde_score.diameter_mm.toFixed(1)} mm
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Risk Assessment */}
              {result.risk_assessment && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-2">Risk Assessment</h3>
                  <div className={`p-4 rounded-lg ${
                    result.risk_assessment.overall_risk === 'high' ? 'bg-red-50' :
                    result.risk_assessment.overall_risk === 'medium' ? 'bg-yellow-50' :
                    'bg-green-50'
                  }`}>
                    <p className="font-semibold mb-2">
                      Risk Level: <span className="uppercase">
                        {result.risk_assessment.overall_risk}
                      </span>
                    </p>
                    <p className="text-sm mb-2">{result.recommendation}</p>
                  </div>
                </div>
              )}

              {/* Grad-CAM Visualization */}
              {result.visualization?.gradcam_path && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-2">AI Attention Map</h3>
                  <img
                    src={`http://localhost:8000${result.visualization.gradcam_path}`}
                    alt="Grad-CAM"
                    className="w-full max-w-md mx-auto rounded-lg"
                  />
                  <p className="text-sm text-gray-600 mt-2 text-center">
                    Highlighted areas show where the AI focused its analysis
                  </p>
                </div>
              )}

              <div className="flex gap-4">
                <button onClick={handleNewAnalysis} className="flex-1 btn-primary">
                  New Analysis
                </button>
                <button onClick={() => navigate('/history')} className="flex-1 btn-secondary">
                  View History
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default AnalysisPage
