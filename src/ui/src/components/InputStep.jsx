import React from 'react';
import InputForm from './InputForm';
import FileInput from './FileInput';

const InputStep = ({ formData, setFormData }) => {
    return (
        <div>
            <InputForm formData={formData} setFormData={setFormData} />
            <div className="file-drop-container">
                <FileInput formData={formData} setFormData={setFormData} />
            </div>
        </div>
    )
}

export default InputStep;