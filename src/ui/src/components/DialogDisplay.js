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

  const truncateText = (text, maxLength = 1000) => {
    if (text.length <= maxLength) {
      return text;
    }
    return text.substring(0, maxLength) + '...';
  };

  const formatText = (text, maxWordsPerLine = 30, maxCharsPerLine = 100) => {
    const words = text.split(' ');
    const lines = [];
    let currentLine = '';

    words.forEach(word => {
      if ((currentLine + word).split(' ').length <= maxWordsPerLine && (currentLine + word).length <= maxCharsPerLine) {
        currentLine += `${word} `;
      } else {
        lines.push(currentLine.trim());
        currentLine = `${word} `;
      }
    });

    if (currentLine.length > 0) {
      lines.push(currentLine.trim());
    }

    // Handle case where there are no spaces
    const formattedLines = lines.map(line => {
      if (line.length > maxCharsPerLine) {
        const splitLines = [];
        for (let i = 0; i < line.length; i += maxCharsPerLine) {
          splitLines.push(line.substring(i, i + maxCharsPerLine));
        }
        return splitLines.join('\n');
      }
      return line;
    });

    return formattedLines.join('\n');
  };

  if (!dialog || !dialog.rounds) {
    return <div>No dialog to display.</div>;
  }

  return (
    <div className="dialog-container">
      <h3>Dialog ID: {dialogId}</h3>
      <p>Initial Prompt: {formatText(truncateText(dialog.initial_prompt))}</p>
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
                    {summarizedOutput ? (
                      <pre>{formatText(prompt.summary)}</pre>
                    ) : (
                      <pre>{formatText(prompt.output)}</pre>
                    )} <br />
                    <strong>Confidence score:</strong> {prompt.conf_score / 10} / 10 <br />
                    <span onClick={() => setSummarizedOutput(!summarizedOutput)}>{summarizedOutput ? 'Show full output' : 'Show summarized output'}</span>
                    <span onClick={() => handleToggleInfo(roundId, index)}>
                      {expandedInfo[roundId]?.[index] ? 'Hide model and input' : 'Show model and input'}
                    </span>
                    {expandedInfo[roundId]?.[index] && (
                      <div>
                        <strong>Model:</strong> {prompt.model} <br />
                        <strong>Input:</strong> {formatText(prompt.input)}
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