import React, { useState, useRef } from "react";
import uploadIcon from '../icons/upload.png';


const FileInput = ({ formData, setFormData }) => {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setFormData((prevState) => ({
        ...prevState,
        file: file,
        fileName: file.name,
      }));
    }
  };

  const handleClick = () => {
    inputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setFormData((prevState) => ({
      ...prevState,
      file: file,
      fileName: file.name,
    }));
  };

  const handleRemoveFile = (e) => {
    e.stopPropagation();
    setFormData((prevState) => ({
      ...prevState,
      file: null,
      fileName: '',
    }));
  };

  return (
    <div
      className={`drop-zone ${isDragging ? "drag-over" : ""}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
    >
      <p>
        {formData.fileName ? (
          <>
            <span className="file-name">{formData.fileName}</span>
            <span className="remove-file" onClick={handleRemoveFile}>
              ✖ {/* Peruuta-symboli */}
            </span>
          </>
        ) : (
          <>
            <img src={uploadIcon} alt="Upload icon" className="upload-icon" /> {/* Lisää ikoni */}
            Drop file or click to upload
          </>
        )}
      </p>
      <input
        type="file"
        ref={inputRef}
        onChange={handleFileChange}
        className="file-input-hidden"
      />
    </div>
  );
};

export default FileInput;
