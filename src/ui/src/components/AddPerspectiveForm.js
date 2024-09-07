import React, { useState } from 'react';

const AddAgentForm = ({ perspectives, setPerspectives }) => {
  const [perspective, setPerspective] = useState('');

  const handleAddPerspective = () => {
    setPerspectives([...perspectives, perspective]);
    setPerspective(''); // Tyhjennä input-kenttä
  };

  return (
    <div>
      <label>Enter a new perspective: </label>
      <input 
        type="text" 
        value={perspective} 
        onChange={(e) => setPerspective(e.target.value)} 
      />
      <button onClick={handleAddPerspective}>Add Perspective</button>
    </div>
  );
};

export default AddAgentForm;