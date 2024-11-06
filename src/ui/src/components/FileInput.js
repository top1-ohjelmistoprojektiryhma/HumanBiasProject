import React from "react";

const FileInput = ({ setPrompt }) => {

    return (
        <div className="input-form-container">
            <input
                type="file"
                onChange={(e) => setPrompt(e.target.files[0])}
                className="input-form"
            />
        </div>
    );
}

export default FileInput;