import React, { useState } from 'react';

const GenerateAgents = ({ onSubmit }) => {
  const [numAgents, setNumAgents] = useState(3); // Default to 3 agents

  const handleSubmit = () => {
    onSubmit(numAgents); // Pass the number of agents to the parent component
  };

  return (
    <div className="generate-agents-container">
      <label htmlFor="numAgents" className="label">
        Number of Agents:
      </label>
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
      <button onClick={handleSubmit} className="generate-button">
        Generate Agents
      </button>
    </div>
  );
};

export default GenerateAgents;
