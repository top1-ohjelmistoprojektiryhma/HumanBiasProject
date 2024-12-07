import React from 'react';

const SummaryToggle = ({ formData, setFormData }) => {
  const handleToggle = () => {
    setFormData({
      ...formData,
      summaryEnabled: !formData.summaryEnabled,
    });
  };

  return (
    <div className="summary-toggle">
      <label className="toggle-label" htmlFor="summary-toggle-checkbox">
        <span className="toggle-text">Summarise text to decrease token usage</span>
        <input
          id="summary-toggle-checkbox"
          type="checkbox"
          checked={formData.summaryEnabled}
          onChange={handleToggle}
        />
        <span className="slider"></span>
      </label>
    </div>
  );
};

export default SummaryToggle;
