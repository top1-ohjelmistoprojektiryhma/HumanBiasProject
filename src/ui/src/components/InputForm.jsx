// src/components/InputForm.jsx
import React, { useEffect, useRef } from 'react';
import uploadIcon from '../icons/paperclip.png'; // Varmista, että polku on oikea

/**
 * InputForm component allows users to enter a statement.
 * Expands as the user types.
 * 
 * @component
 * @param {object} formData - The current form data.
 * @param {Function} setFormData - Function to update the form data.
 */
const InputForm = ({ formData, setFormData }) => {
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);

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
    setFormData((prevState) => ({
      ...prevState,
      text: e.target.value
    }));
  };

  const handleIconClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData((prevState) => ({
        ...prevState,
        file,
        fileName: file.name,
        text: prevState.text // Säilyttää nykyisen tekstin
      }));
    }
  };

  return (
    <div className="input-form-container">
      <textarea
        ref={textareaRef}
        value={formData.text}
        onInput={handleInput}
        placeholder="Enter your statement"
        className="input-form"
        rows="1" // Start with one row
      />
      {formData.fileName && (
        <span className="file-name-overlay">
          {formData.fileName}
        </span>
      )}
      <img
        src={uploadIcon}
        alt="Upload"
        className="upload-icon"
        onClick={handleIconClick}
      />
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="file-input-hidden"
        accept=".txt,.pdf,.docx,.odt" // Rajoita tiedostotyyppiä tarpeen mukaan
      />
    </div>
  );
};

export default InputForm;
