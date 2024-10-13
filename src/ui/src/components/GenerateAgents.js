import React, { useState } from 'react';

const GenerateAgents = ({ onSubmit, perspectives, setPerspectives }) => {
  const [numAgents, setNumAgents] = useState(3); // Default to 3 agents
  const [perspective, setPerspective] = useState('');

  const handleSubmit = () => {
    onSubmit(numAgents); // Pass the number of agents to the parent component
  };

  const handleAddPerspective = async () => {
    if (perspective.trim() === '') return;

    // Lisää uusi perspektiivi paikalliseen tilaan
    setPerspectives([...perspectives, perspective]);

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

      setPerspective(''); // Clear the input field after adding the perspective
    } catch (error) {
      console.error('Error adding perspective:', error);
    }
  };

  return (
    <div className="generate-agents-container">
      {/* Dropdown for selecting the number of agents */}
      <select
        id="numAgents"
        value={numAgents}
        onChange={(e) => setNumAgents(parseInt(e.target.value))}
        className="select-dropdown"
      >
        {[...Array(5)].map((_, i) => (
          <option key={i} value={i + 1}>
            {i + 1}
          </option>
        ))}
      </select>

      {/* Button for generating agents */}
      <button onClick={handleSubmit} className="generate-button">
        Generate Agents
      </button>

      {/* Input field for adding new perspective */}
      <input
        type="text"
        value={perspective}
        onChange={(e) => setPerspective(e.target.value)}
        placeholder="Enter a new perspective"
        className="add-perspective-form"
      />

      {/* Button to add the new perspective */}
      <button onClick={handleAddPerspective} className="add-perspective-button">
        Add Perspective
      </button>
    </div>
  );
};

export default GenerateAgents;
