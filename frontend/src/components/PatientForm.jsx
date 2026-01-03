import { useState } from 'react'

function PatientForm({ onSubmit, loading }) {
  const [condition, setCondition] = useState('')
  const [age, setAge] = useState('')
  const [gender, setGender] = useState('male')
  const [smokingStatus, setSmokingStatus] = useState('never')
  const [pregnancyStatus, setPregnancyStatus] = useState(false)

  const [conditions, setConditions] = useState([])
  const [medications, setMedications] = useState([])
  const [labResults, setLabResults] = useState([])

  const handleSubmit = (e) => {
    e.preventDefault()

    const patientData = {
      age: parseInt(age),
      gender,
      conditions,
      medications,
      lab_results: labResults,
      smoking_status: smokingStatus,
      pregnancy_status: gender === 'female' ? pregnancyStatus : null
    }

    onSubmit(patientData, condition)
  }

  const addCondition = () => {
    setConditions([...conditions, { name: '', icd10_code: '', onset_date: null }])
  }

  const updateCondition = (index, field, value) => {
    const updated = [...conditions]
    updated[index][field] = value || null
    setConditions(updated)
  }

  const removeCondition = (index) => {
    setConditions(conditions.filter((_, i) => i !== index))
  }

  const addMedication = () => {
    setMedications([...medications, { name: '', dosage: '', frequency: '' }])
  }

  const updateMedication = (index, field, value) => {
    const updated = [...medications]
    updated[index][field] = value || null
    setMedications(updated)
  }

  const removeMedication = (index) => {
    setMedications(medications.filter((_, i) => i !== index))
  }

  const addLabResult = () => {
    setLabResults([...labResults, { test_name: '', value: '', unit: '', date: null }])
  }

  const updateLabResult = (index, field, value) => {
    const updated = [...labResults]
    if (field === 'value') {
      updated[index][field] = value ? parseFloat(value) : null
    } else {
      updated[index][field] = value || null
    }
    setLabResults(updated)
  }

  const removeLabResult = (index) => {
    setLabResults(labResults.filter((_, i) => i !== index))
  }

  return (
    <div className="card">
      <form onSubmit={handleSubmit}>
        <h2 className="section-title">Search Criteria</h2>
        <div className="form-group">
          <label>Medical Condition to Search *</label>
          <input
            type="text"
            value={condition}
            onChange={(e) => setCondition(e.target.value)}
            placeholder="e.g., Type 2 Diabetes, Breast Cancer, COPD"
            required
          />
          <small style={{ color: '#6b7280', marginTop: '0.25rem', display: 'block' }}>
            This will search ClinicalTrials.gov for relevant trials
          </small>
        </div>

        <h2 className="section-title" style={{ marginTop: '2rem' }}>Patient Demographics</h2>
        <div className="form-row">
          <div className="form-group">
            <label>Age (years) *</label>
            <input
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              min="0"
              max="120"
              required
            />
          </div>

          <div className="form-group">
            <label>Gender *</label>
            <select value={gender} onChange={(e) => setGender(e.target.value)} required>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Smoking Status</label>
            <select value={smokingStatus} onChange={(e) => setSmokingStatus(e.target.value)}>
              <option value="never">Never</option>
              <option value="former">Former</option>
              <option value="current">Current</option>
            </select>
          </div>

          {gender === 'female' && (
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={pregnancyStatus}
                  onChange={(e) => setPregnancyStatus(e.target.checked)}
                  style={{ marginRight: '0.5rem' }}
                />
                Currently Pregnant
              </label>
            </div>
          )}
        </div>

        <h2 className="section-title" style={{ marginTop: '2rem' }}>Medical Conditions</h2>
        <div className="array-input">
          {conditions.map((cond, index) => (
            <div key={index} className="array-input-item">
              <button
                type="button"
                className="remove-btn"
                onClick={() => removeCondition(index)}
              >
                Remove
              </button>
              <div className="form-group">
                <label>Condition Name *</label>
                <input
                  type="text"
                  value={cond.name}
                  onChange={(e) => updateCondition(index, 'name', e.target.value)}
                  placeholder="e.g., Type 2 Diabetes Mellitus"
                  required
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>ICD-10 Code</label>
                  <input
                    type="text"
                    value={cond.icd10_code || ''}
                    onChange={(e) => updateCondition(index, 'icd10_code', e.target.value)}
                    placeholder="e.g., E11.9"
                  />
                </div>
                <div className="form-group">
                  <label>Onset Date</label>
                  <input
                    type="date"
                    value={cond.onset_date || ''}
                    onChange={(e) => updateCondition(index, 'onset_date', e.target.value)}
                  />
                </div>
              </div>
            </div>
          ))}
          <button type="button" className="add-btn" onClick={addCondition}>
            + Add Condition
          </button>
        </div>

        <h2 className="section-title" style={{ marginTop: '2rem' }}>Current Medications</h2>
        <div className="array-input">
          {medications.map((med, index) => (
            <div key={index} className="array-input-item">
              <button
                type="button"
                className="remove-btn"
                onClick={() => removeMedication(index)}
              >
                Remove
              </button>
              <div className="form-group">
                <label>Medication Name *</label>
                <input
                  type="text"
                  value={med.name}
                  onChange={(e) => updateMedication(index, 'name', e.target.value)}
                  placeholder="e.g., Metformin"
                  required
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Dosage</label>
                  <input
                    type="text"
                    value={med.dosage || ''}
                    onChange={(e) => updateMedication(index, 'dosage', e.target.value)}
                    placeholder="e.g., 500mg"
                  />
                </div>
                <div className="form-group">
                  <label>Frequency</label>
                  <input
                    type="text"
                    value={med.frequency || ''}
                    onChange={(e) => updateMedication(index, 'frequency', e.target.value)}
                    placeholder="e.g., twice daily"
                  />
                </div>
              </div>
            </div>
          ))}
          <button type="button" className="add-btn" onClick={addMedication}>
            + Add Medication
          </button>
        </div>

        <h2 className="section-title" style={{ marginTop: '2rem' }}>Laboratory Results</h2>
        <div className="array-input">
          {labResults.map((lab, index) => (
            <div key={index} className="array-input-item">
              <button
                type="button"
                className="remove-btn"
                onClick={() => removeLabResult(index)}
              >
                Remove
              </button>
              <div className="form-row">
                <div className="form-group">
                  <label>Test Name *</label>
                  <input
                    type="text"
                    value={lab.test_name}
                    onChange={(e) => updateLabResult(index, 'test_name', e.target.value)}
                    placeholder="e.g., HbA1c, Glucose"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Value *</label>
                  <input
                    type="number"
                    step="0.01"
                    value={lab.value}
                    onChange={(e) => updateLabResult(index, 'value', e.target.value)}
                    placeholder="e.g., 7.5"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Unit *</label>
                  <input
                    type="text"
                    value={lab.unit}
                    onChange={(e) => updateLabResult(index, 'unit', e.target.value)}
                    placeholder="e.g., %, mg/dL"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Date</label>
                  <input
                    type="date"
                    value={lab.date || ''}
                    onChange={(e) => updateLabResult(index, 'date', e.target.value)}
                  />
                </div>
              </div>
            </div>
          ))}
          <button type="button" className="add-btn" onClick={addLabResult}>
            + Add Lab Result
          </button>
        </div>

        <div style={{ marginTop: '2rem', textAlign: 'center' }}>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Searching & Matching...' : 'Find Matching Trials'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default PatientForm
