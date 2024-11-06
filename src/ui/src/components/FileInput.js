import React from "react";

const FileInput = ({ setFile }) => {

    return (
        <div className="input-form-container">
            <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="input-form"
            />
        </div>
    );
}

export default FileInput;