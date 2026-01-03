import { useState } from 'react'
import axios from 'axios'
import PatientForm from './components/PatientForm'
import MatchResults from './components/MatchResults'

function App() {
  const [matches, setMatches] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (patientData, condition) => {
    setLoading(true)
    setError(null)
    setMatches(null)

    try {
      const response = await axios.post(
        `/api/matching/match?condition=${encodeURIComponent(condition)}&max_trials=10&min_score=0.0`,
        patientData
      )

      setMatches(response.data)
    } catch (err) {
      console.error('Error matching patient:', err)
      setError(
        err.response?.data?.detail ||
        'An error occurred while matching. Please check your API configuration and try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setMatches(null)
    setError(null)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Clinical Trial Matcher</h1>
        <p>AI-Powered Patient-Trial Matching Using Real Clinical Data</p>
      </div>

      {error && (
        <div className="card">
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        </div>
      )}

      {!matches && !loading && (
        <PatientForm onSubmit={handleSubmit} loading={loading} />
      )}

      {loading && (
        <div className="card">
          <div className="loading">
            <div>Searching clinical trials and analyzing eligibility...</div>
            <div style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
              This may take 30-60 seconds as we query ClinicalTrials.gov and analyze each trial's criteria.
            </div>
          </div>
        </div>
      )}

      {matches && !loading && (
        <MatchResults matches={matches} onReset={handleReset} />
      )}
    </div>
  )
}

export default App
