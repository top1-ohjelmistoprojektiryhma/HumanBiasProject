import React, { useState } from 'react';

const GenerateAgents = ({ onSubmit }) => {
  const [numAgents, setNumAgents] = useState(3); // Default to 3 agents

  const handleSubmit = () => {
    onSubmit(numAgents); // Pass the number of agents to the parent component
  };

  return (
    <div>
      <label htmlFor="numAgents">Number of Agents: </label>
      <select
        id="numAgents"
        value={numAgents}
        onChange={(e) => setNumAgents(parseInt(e.target.value))}
      >
        <option value={1}>1</option>
        <option value={2}>2</option>
        <option value={3}>3</option>
        <option value={4}>4</option>
        <option value={5}>5</option>
      </select>
      <button onClick={handleSubmit}>Generate Agents</button>
    </div>
  );
};

export default GenerateAgents;
