
import React from 'react';

const FormatSelector = ({ setSelectedFormat }) => {
  const handleFormatChange = (e) => {
    setSelectedFormat(e.target.value);
  };

  return (
    <div>
      <label htmlFor="format-select">Select Format:</label>
      <select id="format-select" onChange={handleFormatChange}>
        <option value="dialog">Dialog</option>
        {/* Add other formats as needed */}
      </select>
    </div>
  );
};

export default FormatSelector;
