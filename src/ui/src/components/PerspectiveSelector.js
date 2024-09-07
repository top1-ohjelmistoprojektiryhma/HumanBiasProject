import React from 'react';

const PerspectiveSelector = ({ perspectives, selectedPerspectives, setSelectedPerspectives, setPerspectives }) => {
  const handleCheckboxChange = (perspective) => {
    if (selectedPerspectives.includes(perspective)) {
      setSelectedPerspectives(selectedPerspectives.filter(p => p !== perspective));
    } else {
      setSelectedPerspectives([...selectedPerspectives, perspective]);
    }
  };

  const handleDeletePerspective = (perspective) => {
    setPerspectives(perspectives.filter(p => p !== perspective));
    setSelectedPerspectives(selectedPerspectives.filter(p => p !== perspective));
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
          <button onClick={() => handleDeletePerspective(perspective)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

export default PerspectiveSelector;
