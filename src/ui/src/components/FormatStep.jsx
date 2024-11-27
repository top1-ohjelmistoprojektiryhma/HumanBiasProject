import React from 'react';

const FormatStep = ({ formData, setFormData }) => {
  const handleFormatChange = (event) => {
    setFormData({
      ...formData,
      selectedFormat: event.target.value,
    });
  };

  return (
    <div className='format-selector'>
      <h2>Select Format</h2>
      {formData.formatOptions.length > 0 ? (
        <select
          value={formData.selectedFormat}
          onChange={handleFormatChange}
        >
          {formData.formatOptions.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
      ) : (
        <p>Loading formats...</p>
      )}
    </div>
  );
};

export default FormatStep;
