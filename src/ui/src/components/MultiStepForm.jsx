import React, { useState } from "react";
import InputStep from "./InputStep";
import FormatStep from "./FormatStep";
import AgentStep from "./AgentStep";

const MultiStepForm = ({ getPromptSummary, onGenerateAgents, onSubmit, formData, setFormData, loading }) => {
    const [currentStep, setCurrentStep] = useState(1);

    const nextStep = async () => {
        let step = currentStep;
        setCurrentStep((prev) => prev + 1);
        if (step === 1 && formData.agentOptions.length === 0) {
            let promptSummary = await getPromptSummary();
            console.log(promptSummary)
            onGenerateAgents(3, promptSummary, true)
        }
    };
    const prevStep = () => setCurrentStep((prev) => prev - 1);

    const renderStep = () => {
        switch (currentStep) {
            case 1:
                return <InputStep formData={formData} setFormData={setFormData} />;
            case 2:
                return <FormatStep formData={formData} setFormData={setFormData} />;
            case 3:
                return <AgentStep onGenerate={onGenerateAgents} formData={formData} setFormData={setFormData} loading={loading} />;
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
