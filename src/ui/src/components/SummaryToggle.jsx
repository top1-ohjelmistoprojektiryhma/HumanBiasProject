import React from 'react';

const SummaryToggle = ({ summaryEnabled, setSummaryEnabled }) => {
  const handleToggle = () => {
    setSummaryEnabled((prev) => !prev);
  };

  return (
    <div className="summary-toggle">
      <label className="toggle-label" htmlFor="summary-toggle-checkbox">
        <span className="toggle-text">Improve performance by summarizing data</span>
        <input
          id="summary-toggle-checkbox"
          type="checkbox"
          checked={summaryEnabled}
          onChange={handleToggle}
        />
        <span className="slider"></span>
      </label>
    </div>
  );
};

export default SummaryToggle;
