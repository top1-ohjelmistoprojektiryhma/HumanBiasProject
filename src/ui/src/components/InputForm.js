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
      {/* Input field with placeholder */}
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your statement"
        className="input-form"
      />
    </div>
  );
};

export default InputForm;
