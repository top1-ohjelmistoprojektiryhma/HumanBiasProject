import React from 'react';

/**
 * PerspectiveSelector component allows users to select perspectives by clicking on boxes.
 * 
 * @component
 * @param {Array} perspectives - The list of available perspectives.
 * @param {Array} selectedPerspectives - The list of currently selected perspectives.
 * @param {Function} setSelectedPerspectives - Function to update the selected perspectives.
 */
const PerspectiveSelector = ({ perspectives, selectedPerspectives, setSelectedPerspectives, setPerspectives }) => {

  /**
   * Handle agent click event.
   * 
   * Toggles the perspective selection when the user clicks on the agent box.
   * 
   * @param {string} perspective - The perspective to select or deselect.
   */
  const handleAgentClick = (perspective) => {
    if (selectedPerspectives.includes(perspective)) {
      setSelectedPerspectives(selectedPerspectives.filter(p => p !== perspective));
    } else {
      setSelectedPerspectives([...selectedPerspectives, perspective]);
    }
  };

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
    <div className="perspective-selector-container">
      <label>Select perspectives:</label>

      <div className="agent-box-container">
        {perspectives.map((perspective, index) => (
          <div
            key={index}
            className={`agent-box ${selectedPerspectives.includes(perspective) ? 'active' : ''}`}
            onClick={() => handleAgentClick(perspective)}
          >
            {perspective}
            <button onClick={() => handleDeletePerspective(perspective)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PerspectiveSelector;
