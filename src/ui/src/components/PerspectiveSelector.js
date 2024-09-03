import React from 'react';

const PerspectiveSelector = ({ perspectives, setSelectedPerspective }) => {
  return (
    <div>
      <label>Select a perspective:</label>
      <select onChange={(e) => setSelectedPerspective(e.target.value)}>
        {perspectives.map((perspective, index) => (
          <option key={index} value={perspective}>
            {perspective}
          </option>
        ))}
      </select>
    </div>
  );
};

export default PerspectiveSelector;
