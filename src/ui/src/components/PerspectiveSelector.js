import React from 'react';

const PerspectiveSelector = ({ perspectives, selectedPerspectives, setSelectedPerspectives }) => {
  const handleCheckboxChange = (perspective) => {
    if (selectedPerspectives.includes(perspective)) {
      setSelectedPerspectives(selectedPerspectives.filter(p => p !== perspective));
    } else {
      setSelectedPerspectives([...selectedPerspectives, perspective]);
    }
  };

  return (
    <div>
      <label>Select perspectives:</label>
      {perspectives.map((perspective, index) => (
        <div key={index}>
          <input
            type="checkbox"
            value={perspective}
            checked={selectedPerspectives.includes(perspective)}
            onChange={() => handleCheckboxChange(perspective)}
          />
          {perspective}
        </div>
      ))}
    </div>
  );
};

export default PerspectiveSelector;
