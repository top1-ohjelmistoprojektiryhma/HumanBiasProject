import React, { useState } from 'react';

const DialogsBar = ({ dialogs, toggleDialog }) => {

  const handleToggleDialog = (dialogId) => {
    toggleDialog(dialogId);
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
                Dialog {dialogId}: {dialogs[dialogId].initial_prompt.substring(0, 50)}...
              </strong>
            </li>
          )))}
      </ul >
    </div >
  );
};

export default DialogsBar;


