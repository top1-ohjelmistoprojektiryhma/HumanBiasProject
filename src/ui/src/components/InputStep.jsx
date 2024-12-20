// src/components/InputForm.jsx
import React, { useEffect, useRef } from 'react';
import uploadIcon from '../icons/paperclip.png';

/**
 * InputForm component allows users to enter a statement.
 * Expands as the user types.
 * 
 * @component
 * @param {object} formData - The current form data.
 * @param {Function} setFormData - Function to update the form data.
 */
const InputStep = ({ formData, setFormData }) => {
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
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
        text: prevState.text
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
        <div className="file-name-overlay">
        <span className="file-name-text">{formData.fileName}</span>
        <button
          className="delete-file-button"
          onClick={() => {
            setFormData((prevState) => ({
              ...prevState,
              file: null,
              fileName: null,
            }));
          }}
        >
          &times;
        </button>
      </div>
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
        accept=".txt,.pdf,.docx,.odt"
      />
    </div>
  );
};

export default InputStep;
