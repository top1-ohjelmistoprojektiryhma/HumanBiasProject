import React from 'react';

/**
 * InputForm component allows users to enter a statement.
 * 
 * @component
 * @param {string} prompt - The current value of the input field.
 * @param {Function} setPrompt - Function to update the value of the input field.
 */
const InputForm = ({ prompt, setPrompt }) => {
  return (
    <div>
      {/* Label for the input field */}
      <label>Enter your statement:</label>

      {/* Input field for entering the statement */}
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
    </div>
  );
};

export default InputForm;
