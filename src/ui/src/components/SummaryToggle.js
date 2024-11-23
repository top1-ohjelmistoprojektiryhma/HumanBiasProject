import React from 'react';

const SummaryToggle = ({ summaryEnabled, setSummaryEnabled }) => {
  const handleToggle = () => {
    setSummaryEnabled((prev) => !prev);
  };

  return (
    <div className="summary-toggle">
      <label htmlFor="summary-toggle-checkbox">
        Enable Summary
        <input
          id="summary-toggle-checkbox"
          type="checkbox"
          checked={summaryEnabled}
          onChange={handleToggle}
        />
      </label>
    </div>
  );
};

export default SummaryToggle;
