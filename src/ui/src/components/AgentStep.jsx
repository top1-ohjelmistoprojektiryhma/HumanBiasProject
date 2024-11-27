import React from "react";
import GenerateAgents from "./GenerateAgents";
import PerspectiveSelector from "./PerspectiveSelector";

const AgentStep = ({ onGenerate, formData, setFormData }) => {
    return (
        <div>
            <div className="generate-agents-container">
                <GenerateAgents onGenerate={onGenerate} formData={formData} setFormData={setFormData} />
            </div>
            <PerspectiveSelector formData={formData} setFormData={setFormData} />

        </div >
    )
}

export default AgentStep