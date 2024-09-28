import React, { useState } from 'react';

const DialogsBar = ({ dialogs, expandedDialogs, toggleDialog }) => {
  const [expandedRounds, setExpandedRounds] = useState({});

  const handleToggleDialog = (dialogId) => {
    toggleDialog((prevState) => ({
      ...prevState,
      [dialogId]: !prevState[dialogId],
    }));
  };

  const handleToggleRound = (dialogId, roundId) => {
    setExpandedRounds((prevState) => ({
      ...prevState,
      [dialogId]: {
        ...prevState[dialogId],
        [roundId]: !prevState[dialogId]?.[roundId],
      },
    }));
  };

  return (
    <div className="dialogs-bar">
      <h2>Dialogs</h2>
      <ul>
        {Object.keys(dialogs).length === 0 ? (
          <p>No dialogs available.</p>
        ) : (
          Object.keys(dialogs).map((dialogId) => (
            <li key={dialogId}>
              <strong onClick={() => handleToggleDialog(dialogId)} style={{ cursor: 'pointer' }}>
                Dialog {dialogId}: {dialogs[dialogId].initial_prompt}
              </strong>
              {expandedDialogs[dialogId] && (
                <ul>
                  {Object.keys(dialogs[dialogId].rounds).map((roundId) => (
                    <li key={roundId}>
                      <strong onClick={() => handleToggleRound(dialogId, roundId)} style={{ cursor: 'pointer' }}>
                        Round {roundId}
                      </strong>

                      {expandedRounds[dialogId]?.[roundId] && (
                        <ul>
                          {dialogs[dialogId].rounds[roundId].map((prompt, index) => (
                            <li key={index}>
                              <strong>Agent:</strong> {prompt.agent} <br />
                              <strong>Model:</strong> {prompt.model} <br />
                              <strong>Input:</strong> {prompt.input} <br />
                              <strong>Output:</strong> {prompt.output}
                            </li>
                          ))}
                        </ul>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default DialogsBar;


