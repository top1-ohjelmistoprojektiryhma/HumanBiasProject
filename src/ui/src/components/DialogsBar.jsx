import React, { useState } from 'react';

const DialogsBar = ({ dialogs, openedDialog, setOpenedDialog }) => {

  const handleToggleDialog = (dialogId) => {
    if (openedDialog === dialogId) {
      setOpenedDialog(null);
    } else {
      setOpenedDialog(dialogId);
    }
  }

  return (
    <div className="dialogs-bar">
      <h2>Dialogs</h2>
      <ul>
        {Object.keys(dialogs).length === 0 ? (
          <p>No dialogs available.</p>
        ) : (
          Object.keys(dialogs).map((dialogId) => (
            <li key={dialogId}>
              <p className={openedDialog === dialogId ? "bar-opened-dialog" : "bar-dialog"} onClick={() => handleToggleDialog(dialogId)} style={{ cursor: 'pointer' }}>
                Dialog {dialogId}: {dialogs[dialogId].initial_prompt.substring(0, 50)}...
              </p>
            </li>
          )))}
      </ul >
    </div >
  );
};

export default DialogsBar;


