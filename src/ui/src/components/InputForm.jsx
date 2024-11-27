import React, { useEffect, useRef } from 'react';

/**
 * InputForm component allows users to enter a statement.
 * Expands as the user types.
 * 
 * @component
 * @param {string} prompt - The current value of the input field.
 * @param {Function} setPrompt - Function to update the value of the input field.
 */
const InputForm = ({ prompt, setPrompt }) => {
  const textareaRef = useRef(null);

  useEffect(() => {
    // Aseta alkuperäinen korkeus vastaamaan sisältöä, vaikka se olisi tyhjä.
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, []);

  const handleInput = (e) => {
    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;
    setPrompt(e.target.value);
  };

  return (
    <div className="input-form-container">
      <textarea
        ref={textareaRef}
        value={prompt}
        onInput={handleInput}
        placeholder="Enter your statement"
        className="input-form"
        rows="1" // Start with one row
      />
    </div>
  );
};

export default InputForm;
