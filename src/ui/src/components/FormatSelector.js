import React from 'react';

const FormatSelector = ({ formatOptions, setSelectedFormat }) => {
  const handleFormatChange = (e) => {
    setSelectedFormat(e.target.value);
  };

  return (
    <div>
      <label htmlFor="format-select">Select Format:</label>
      <select id="format-select" onChange={handleFormatChange}>
        {formatOptions.map((format) => (
          <option key={format} value={format}>
            {format}
          </option>
        ))}
      </select>
    </div>
  );
};

export default FormatSelector;