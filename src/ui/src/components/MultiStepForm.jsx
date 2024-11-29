import React, { useState } from "react";
import InputStep from "./InputStep";
import FormatStep from "./FormatStep";
import AgentStep from "./AgentStep";

const MultiStepForm = ({ onGenerate, onSubmit, formData, setFormData }) => {
    const [currentStep, setCurrentStep] = useState(1);

    const nextStep = () => {
        if (currentStep === 1) {
            onGenerate(3, true);
        }
        setCurrentStep((prev) => prev + 1);
    };
    const prevStep = () => setCurrentStep((prev) => prev - 1);

    const renderStep = () => {
        switch (currentStep) {
            case 1:
                return <InputStep formData={formData} setFormData={setFormData} />;
            case 2:
                return <FormatStep formData={formData} setFormData={setFormData} />;
            case 3:
                return <AgentStep onGenerate={onGenerate} formData={formData} setFormData={setFormData} />;
            default:
                return <InputStep formData={formData} setFormData={setFormData} />;
        }
    };

    return (
        <div className="content-container">
            {renderStep()}
            <div className="button-container">
                {currentStep > 1 && (
                    <button className="back-btn" onClick={prevStep}>
                        Back
                    </button>
                )}
                {currentStep < 3 ? (
                    <button className="next-btn" onClick={nextStep}>
                        Next
                    </button>
                ) : (
                    <button className="next-btn" onClick={onSubmit}>
                        Submit
                    </button>
                )}
            </div>
        </div>
    );
    
};

export default MultiStepForm;
