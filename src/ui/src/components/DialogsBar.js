import React from 'react';

const DialogsBar = ({ dialogs, expandedDialogs, toggleDialog }) => {
  // Funktio, joka käsittelee dialogin laajentamisen ja pienentämisen
  const handleToggleDialog = (dialogId) => {
    toggleDialog((prevState) => ({
      ...prevState,
      [dialogId]: !prevState[dialogId], // Käännä tila
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
              {/* Klikattava initial prompt */}
              <strong onClick={() => handleToggleDialog(dialogId)} style={{ cursor: 'pointer' }}>
                Dialog {dialogId}: {dialogs[dialogId].initial_prompt}
              </strong>
              
              {/* Näytä yksityiskohdat vain, jos dialogi on avattu */}
              {expandedDialogs[dialogId] && (
                <ul>
                  {Object.keys(dialogs[dialogId].rounds).map((roundId) => (
                    <li key={roundId}>
                      <strong>Round {roundId}:</strong>
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


