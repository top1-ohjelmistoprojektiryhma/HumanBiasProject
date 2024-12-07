import React from 'react';

const FormatStep = ({ formData, setFormData }) => {
  const handleFormatChange = (event) => {
    setFormData({
      ...formData,
      selectedFormat: event.target.value,
    });
  };

  const getFormatText = (option) => {
    let header = '';
    let description = '';
    switch (option) {
      case 'dialog - no consensus':
        header = 'Dialog - No Consensus';
        description = 'This format emphasizes maintaining strong individual perspectives and debating without necessarily finding common ground.';
        return { header, description };
      case 'dialog - consensus':
        header = 'Dialog - Consensus';
        description = 'In this format, the primary goal is to reach an agreement or find common ground on the discussed topic.'
        return { header, description };
      case 'bias finder':
        header = 'Bias Finder';
        description = 'The Bias Finder format is designed to identify and analyze biases in text.';
        return { header, description };
      default: 'dialog - no consensus';
        header = 'Dialog - No Consensus';
        description = 'This format emphasizes maintaining strong individual perspectives and debating without necessarily finding common ground.';
        return { header, description };
    };
  };

  return (
    <div className='format-selector'>
      <h2>Select Format</h2>
      {formData.formatOptions.length > 0 ? (
        <div className='format-selector'>
          {formData.formatOptions.map((option, index) => {
            const { header, description } = getFormatText(option);
            return (
              <label key={index} style={{ display: 'block', marginBottom: '8px' }}>
                <input className='format-radio'
                  type="radio"
                  value={option}
                  checked={formData.selectedFormat === option}
                  onChange={handleFormatChange}
                />
                <strong>{header}</strong>
                <p>{description}</p>
              </label>
            );
          })}
        </div>) : (
        <p>Loading formats...</p>
      )}
    </div>
  );
};

export default FormatStep;
