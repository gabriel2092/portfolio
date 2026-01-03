import { useState } from 'react'
import axios from 'axios'

function MatchResults({ matches, onReset }) {
  const [exporting, setExporting] = useState(false)

  const getScoreClass = (score) => {
    if (score >= 0.7) return 'score-high'
    if (score >= 0.4) return 'score-medium'
    return 'score-low'
  }

  const exportToCSV = async () => {
    setExporting(true)
    try {
      const response = await axios.post('/api/matching/export/csv', matches, {
        responseType: 'blob'
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'trial_matches.csv')
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Error exporting CSV:', error)
      alert('Failed to export CSV')
    } finally {
      setExporting(false)
    }
  }

  const exportToJSON = async () => {
    setExporting(true)
    try {
      const response = await axios.post('/api/matching/export/json', matches, {
        responseType: 'blob'
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'trial_matches.json')
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Error exporting JSON:', error)
      alert('Failed to export JSON')
    } finally {
      setExporting(false)
    }
  }

  if (!matches || matches.length === 0) {
    return (
      <div className="card">
        <h2>No Matches Found</h2>
        <p style={{ marginTop: '1rem', color: '#6b7280' }}>
          No clinical trials were found matching the patient's criteria. Try adjusting the search condition or patient parameters.
        </p>
        <button onClick={onReset} className="btn btn-primary" style={{ marginTop: '1rem' }}>
          Try Another Search
        </button>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="results-header">
        <h2>Match Results ({matches.length} trials)</h2>
        <div className="export-buttons">
          <button
            onClick={exportToCSV}
            className="btn btn-secondary btn-small"
            disabled={exporting}
          >
            Export CSV
          </button>
          <button
            onClick={exportToJSON}
            className="btn btn-secondary btn-small"
            disabled={exporting}
          >
            Export JSON
          </button>
          <button onClick={onReset} className="btn btn-secondary btn-small">
            New Search
          </button>
        </div>
      </div>

      {matches.map((match, index) => (
        <div key={index} className="match-card">
          <div className="match-header">
            <div className="match-title">
              <h3>{match.trial.title}</h3>
              <div className="nct-id">
                NCT ID: {match.trial.nct_id}
                {match.trial.phase && ` • ${match.trial.phase}`}
                {match.trial.status && ` • ${match.trial.status}`}
              </div>
            </div>
            <div className="match-score">
              <div className={`score-badge ${getScoreClass(match.match_score)}`}>
                {(match.match_score * 100).toFixed(0)}%
              </div>
              <div>
                <span className={`eligibility-badge ${match.is_eligible ? 'eligible' : 'not-eligible'}`}>
                  {match.is_eligible ? 'Eligible' : 'Not Eligible'}
                </span>
              </div>
            </div>
          </div>

          {match.trial.brief_summary && (
            <div style={{ marginBottom: '1rem', color: '#6b7280', lineHeight: '1.6' }}>
              {match.trial.brief_summary.substring(0, 300)}
              {match.trial.brief_summary.length > 300 ? '...' : ''}
            </div>
          )}

          <div className="explanation">
            <strong>Match Explanation:</strong>
            <div style={{ marginTop: '0.5rem' }}>{match.explanation}</div>
          </div>

          {match.inclusion_matches && match.inclusion_matches.length > 0 && (
            <div className="criteria-section">
              <h4>✓ Inclusion Criteria Met ({match.inclusion_matches.length})</h4>
              <ul className="criteria-list matches">
                {match.inclusion_matches.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {match.inclusion_mismatches && match.inclusion_mismatches.length > 0 && (
            <div className="criteria-section">
              <h4>✗ Inclusion Criteria Not Met ({match.inclusion_mismatches.length})</h4>
              <ul className="criteria-list mismatches">
                {match.inclusion_mismatches.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {match.exclusion_violations && match.exclusion_violations.length > 0 && (
            <div className="criteria-section">
              <h4>✗ Exclusion Criteria Violated ({match.exclusion_violations.length})</h4>
              <ul className="criteria-list mismatches">
                {match.exclusion_violations.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {match.exclusion_passes && match.exclusion_passes.length > 0 && (
            <div className="criteria-section">
              <h4>✓ Exclusion Criteria Passed ({match.exclusion_passes.length})</h4>
              <ul className="criteria-list passes">
                {match.exclusion_passes.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {match.trial.locations && match.trial.locations.length > 0 && (
            <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#6b7280' }}>
              <strong>Locations:</strong> {match.trial.locations.join(', ')}
            </div>
          )}

          {match.trial.interventions && match.trial.interventions.length > 0 && (
            <div style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#6b7280' }}>
              <strong>Interventions:</strong> {match.trial.interventions.join(', ')}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

export default MatchResults
