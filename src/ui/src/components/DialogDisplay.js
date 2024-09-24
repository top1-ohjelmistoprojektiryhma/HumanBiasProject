import React, { useState, useEffect } from 'react';

const DialogDisplay = ({ dialogId, dialog }) => {
  const [expandedRounds, setExpandedRounds] = useState({});

  useEffect(() => {
    if (dialog && dialog.rounds) {
      const latestRoundId = Math.max(...Object.keys(dialog.rounds).map(Number));
      setExpandedRounds({ [latestRoundId]: true });
    }
  }, [dialog]);

  const handleToggleRound = (roundId) => {
    setExpandedRounds((prevState) => ({
      ...prevState,
      [roundId]: !prevState[roundId],
    }));
  };

  if (!dialog || !dialog.rounds) {
    return <div>No dialog to display.</div>;
  }

  return (
    <div>
      <h3>Dialog ID: {dialogId}</h3>
      <p>Initial Prompt: {dialog.initial_prompt}</p>
      <div>
        {Object.keys(dialog.rounds).map((roundId) => (
          <div key={roundId}>
            <h4 onClick={() => handleToggleRound(roundId)} style={{ cursor: 'pointer' }}>
              Round {parseInt(roundId)}
            </h4>
            {expandedRounds[roundId] && (
              <ul>
                {dialog.rounds[roundId].map((prompt, index) => (
                  <li key={index} style={{ marginBottom: '10px' }}>
                    <strong>Agent:</strong> {prompt.agent.role} <br />
                    <strong>Model:</strong> {prompt.model} <br />
                    <strong>Input:</strong> {prompt.input} <br />
                    <strong>Output:</strong> {prompt.output}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DialogDisplay;