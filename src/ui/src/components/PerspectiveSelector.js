import React from 'react';

const PerspectiveSelector = ({ perspectives, selectedPerspectives, setSelectedPerspectives, setPerspectives }) => {
  const handleCheckboxChange = (perspective) => {
    if (selectedPerspectives.includes(perspective)) {
      setSelectedPerspectives(selectedPerspectives.filter(p => p !== perspective));
    } else {
      setSelectedPerspectives([...selectedPerspectives, perspective]);
    }
  };

  const handleDeletePerspective = async (perspective) => {
    setPerspectives(perspectives.filter(p => p !== perspective));
    setSelectedPerspectives(selectedPerspectives.filter(p => p !== perspective));
    try {
      const response = await fetch('/api/delete-perspective', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ perspective: perspective })
      });
      const result = await response.json();
      console.log('Deleted perspective:', result);
    } catch (error) {
      console.error('Error deleting perspective:', error);
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
          <button onClick={() => handleDeletePerspective(perspective)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

export default PerspectiveSelector;
