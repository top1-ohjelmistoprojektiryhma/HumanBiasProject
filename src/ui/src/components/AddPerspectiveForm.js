import React, { useState } from 'react';

/**
 * AddAgentForm component allows users to add a new perspective.
 * 
 * @component
 * @param {Array} perspectives - The current list of perspectives.
 * @param {Function} setPerspectives - Function to update the list of perspectives.
 */
const AddAgentForm = ({ perspectives, setPerspectives }) => {
  const [perspective, setPerspective] = useState('');

  /**
   * Handle adding a new perspective.
   * 
   * This function sends a POST request to the backend to add a new perspective.
   * If the request is successful, it updates the list of perspectives in the state.
   * 
   * @async
   * @function
   */
  const handleAddPerspective = async () => {
    if (perspective.trim() === '') return;

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
      setPerspective('');
    } catch (error) {
      console.error('Error adding perspective:', error);
    }
  };

  return (
    <div>
      {/* Input field with placeholder */}
      <input
        type="text"
        value={perspective}
        onChange={(e) => setPerspective(e.target.value)}
        placeholder="Enter a new perspective"
        className="add-perspective-form"
      />

      {/* Button to add the new perspective */}
      <button onClick={handleAddPerspective}>Add Perspective</button>
    </div>
  );
};

export default AddAgentForm;
