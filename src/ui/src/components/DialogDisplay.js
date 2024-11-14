import React, { useState, useEffect } from 'react';

const DialogDisplay = ({ dialogId, dialog }) => {
  const [expandedRounds, setExpandedRounds] = useState({});
  const [summarizedOutput, setSummarizedOutput] = useState(true);
  const [expandedInfo, setExpandedInfo] = useState({});

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

  const handleToggleInfo = (roundId, index) => {
    setExpandedInfo((prevState) => ({
      ...prevState,
      [roundId]: {
        ...prevState[roundId],
        [index]: !prevState[roundId]?.[index],
      },
    }));
  };

  const truncatePrompt = (text, maxLength = 1000) => {
    if (text.length <= maxLength) {
      return text;
    }
    return text.substring(0, maxLength) + '...';
  };

  if (!dialog || !dialog.rounds) {
    return <div>No dialog to display.</div>;
  }

  return (
    <div className="dialog-container">
      <h3>Dialog ID: {dialogId}</h3>
      <p>Initial Prompt: {truncatePrompt(dialog.initial_prompt)}</p>
      <div>
        {Object.keys(dialog.rounds).map((roundId) => (
          <div key={roundId} className="dialog-round">
            <h4 onClick={() => handleToggleRound(roundId)}>
              {parseInt(roundId) === 1 ? `Round ${parseInt(roundId)}: Opening statements` : `Round ${parseInt(roundId)}: ${dialog.rounds[roundId][0]?.agent || 'Unknown Agent'}`}
            </h4>
            {expandedRounds[roundId] && (
              <ul>
                {dialog.rounds[roundId].map((prompt, index) => (
                  <li key={index}>
                    <strong>Agent:</strong> {prompt.agent} <br />
                    {summarizedOutput ? (<>{prompt.summary}</>) : (<>{prompt.output}</>)} <br />
                    <strong>Confidence score:</strong> {prompt.conf_score / 10} / 10 <br />
                    <span onClick={() => setSummarizedOutput(!summarizedOutput)}>{summarizedOutput ? 'Show full output' : 'Show summarized output'}</span>
                    <span onClick={() => handleToggleInfo(roundId, index)}>
                      {expandedInfo[roundId]?.[index] ? 'Hide model and input' : 'Show model and input'}
                    </span>
                    {expandedInfo[roundId]?.[index] && (
                      <div>
                        <strong>Model:</strong> {prompt.model} <br />
                        <strong>Input:</strong> {prompt.input} <br />
                      </div>
                    )}
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