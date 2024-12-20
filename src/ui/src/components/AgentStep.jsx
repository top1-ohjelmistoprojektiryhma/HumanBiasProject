import React from "react";
import GenerateAgents from "./GenerateAgents";
import PerspectiveSelector from "./PerspectiveSelector";
import SummaryToggle from "./SummaryToggle";

const AgentStep = ({ onGenerate, formData, setFormData, loading }) => {
    return (
        <div>
            {!loading ? (
                <div>
                    <div className="generate-agents-container">
                        <GenerateAgents onGenerate={onGenerate} formData={formData} setFormData={setFormData} />
                    </div>
                    <PerspectiveSelector formData={formData} setFormData={setFormData} />
                    <SummaryToggle
                        formData={formData}
                        setFormData={setFormData}
                    />
                </div>
            ) : (
                null
            )}
            {loading ? (
                <div className="spinner-container">
                    <div className="spinner"></div>
                </div>
            ) : null}

        </div >
    )
}

export default AgentStep