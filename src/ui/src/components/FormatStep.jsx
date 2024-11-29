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
        <div className='format-selector'>
          {formData.formatOptions.map((option, index) => (
            <label key={index} style={{ display: 'block', marginBottom: '8px' }}>
              <input className='format-radio'
                type="radio"
                value={option}
                checked={formData.selectedFormat === option}
                onChange={handleFormatChange}
              />
              {option}
            </label>
          ))}
        </div>) : (
        <p>Loading formats...</p>
      )}
    </div>
  );
};

export default FormatStep;
