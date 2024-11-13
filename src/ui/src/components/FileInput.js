import React, { useState, useRef } from "react";

const FileInput = ({ setFile }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState(''); // Tila tiedoston nimeä varten
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
      setFile(file);
      setFileName(file.name); // Päivittää tiedoston nimen
    }
  };

  const handleClick = () => {
    inputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFile(file);
      setFileName(file.name); // Päivittää tiedoston nimen
    }
  };

  const handleRemoveFile = (e) => {
    e.stopPropagation(); // Estää drop-zonen onClick-tapahtuman
    setFile(null); // Tyhjentää tiedoston
    setFileName(''); // Tyhjentää tiedoston nimen
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
        {fileName ? (
          <>
            <span className="file-name">{fileName}</span>
            <span className="remove-file" onClick={handleRemoveFile}>
              ✖ {/* Peruuta-symboli */}
            </span>
          </>
        ) : (
          "Drop file or click to upload"
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
