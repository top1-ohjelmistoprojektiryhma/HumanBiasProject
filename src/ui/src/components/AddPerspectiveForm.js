import React, { useState } from 'react';

const AddAgentForm = ({ perspectives, setPerspectives }) => {
  const [perspective, setPerspective] = useState('');

  const handleAddPerspective = async () => {
    if (perspective.trim() === '') return; // Varmista, että perspektiivi ei ole tyhjä

    try {
      const response = await fetch('/api/add-perspective', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ perspective: perspective })
      });
      const result = await response.json();
      console.log('Added perspective:', result);
      setPerspectives([...perspectives, perspective]);
      setPerspective(''); // Tyhjennä syötekenttä onnistuneen lisäyksen jälkeen
    }
    catch (error) {
      console.error('Error adding perspective:', error);
    }
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