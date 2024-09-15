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
    // Ensure the perspective is not empty
    if (perspective.trim() === '') return;

    try {
      // Send POST request to add the new perspective
      const response = await fetch('/api/add-perspective', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ perspective: perspective })
      });
      const result = await response.json();
      console.log('Added perspective:', result);

      // Update the list of perspectives in the state
      setPerspectives([...perspectives, perspective]);

      // Clear the input field after successful addition
      setPerspective('');
    } catch (error) {
      console.error('Error adding perspective:', error);
    }
  };

  return (
    <div>
      {/* Label for the input field */}
      <label>Enter a new perspective: </label>

      {/* Input field for entering a new perspective */}
      <input
        type="text"
        value={perspective}
        onChange={(e) => setPerspective(e.target.value)}
      />

      {/* Button to add the new perspective */}
      <button onClick={handleAddPerspective}>Add Perspective</button>
    </div>
  );
};

export default AddAgentForm;