import React from 'react';

/**
 * PerspectiveSelector component allows users to select and delete perspectives.
 * 
 * @component
 * @param {Array} perspectives - The list of available perspectives.
 * @param {Array} selectedPerspectives - The list of currently selected perspectives.
 * @param {Function} setSelectedPerspectives - Function to update the selected perspectives.
 * @param {Function} setPerspectives - Function to update the list of perspectives.
 */
const PerspectiveSelector = ({ perspectives, selectedPerspectives, setSelectedPerspectives, setPerspectives }) => {
  /**
   * Handle checkbox change event.
   * 
   * Adds or removes the perspective from the selected perspectives list.
   * 
   * @param {string} perspective - The perspective to add or remove.
   */
  const handleCheckboxChange = (perspective) => {
    if (selectedPerspectives.includes(perspective)) {
      setSelectedPerspectives(selectedPerspectives.filter(p => p !== perspective));
    } else {
      setSelectedPerspectives([...selectedPerspectives, perspective]);
    }
  };

  /**
   * Handle delete perspective event.
   * 
   * Sends a request to the backend to delete the perspective and updates the state.
   * 
   * @async
   * @param {string} perspective - The perspective to delete.
   */
  const handleDeletePerspective = async (perspective) => {
    // Update the state to remove the perspective
    setPerspectives(perspectives.filter(p => p !== perspective));
    setSelectedPerspectives(selectedPerspectives.filter(p => p !== perspective));

    try {
      // Send a POST request to delete the perspective
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
      {/* Label for the perspective selection */}
      <label>Select perspectives:</label>

      {/* List of perspectives with checkboxes and delete buttons */}
      {perspectives.map((perspective, index) => (
        <div key={index}>
          {/* Checkbox for selecting a perspective */}
          <input
            type="checkbox"
            value={perspective}
            checked={selectedPerspectives.includes(perspective)}
            onChange={() => handleCheckboxChange(perspective)}
          />
          {perspective}

          {/* Button to delete the perspective */}
          <button onClick={() => handleDeletePerspective(perspective)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

export default PerspectiveSelector;
