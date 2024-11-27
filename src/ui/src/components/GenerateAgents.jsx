import React, { useState } from 'react';
import Button from './common/Button'

const GenerateAgents = ({ onGenerate, formData, setFormData }) => {
  const [numAgents, setNumAgents] = useState(3);
  const [perspective, setPerspective] = useState('');

  const handleSubmit = () => {
    onGenerate(numAgents); // Pass the number of agents to the parent component
  };

  const handleAddPerspective = async () => {
    if (perspective.trim() === '') return;
    let newAgents = [...formData.agentOptions, perspective]
    setFormData((prevState) => ({
      ...prevState,
      agentOptions: newAgents,
    }))
    try {
      const response = await fetch('/api/add-perspective', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ perspective: perspective })
      });
      const result = await response.json();
      setPerspective('');
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
      <Button text="Generate Agents" onClick={handleSubmit} />
      <input
        type="text"
        value={perspective}
        onChange={(e) => setPerspective(e.target.value)}
        placeholder="Enter a new perspective"
        className="add-perspective-form"
      />
      <Button text="Add Perspective" onClick={handleAddPerspective} />
    </div>
  );
};

export default GenerateAgents;
