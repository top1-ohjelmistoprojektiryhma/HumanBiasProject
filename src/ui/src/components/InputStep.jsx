import React from 'react';
import InputForm from './InputForm';
import FileInput from './FileInput';

const InputStep = ({ formData, setFormData }) => {
    return (
        <div className='input-step'>
            <InputForm formData={formData} setFormData={setFormData} />
        </div>
    )
}

export default InputStep;