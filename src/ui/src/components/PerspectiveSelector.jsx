import React from 'react';

const PerspectiveSelector = ({ formData, setFormData }) => {
  const handleAgentClick = (perspective) => {
    const selectedAgents = formData.selectedAgents.includes(perspective)
      ? formData.selectedAgents.filter(p => p !== perspective)
      : [...formData.selectedAgents, perspective];

    setFormData((prevState) => ({
      ...prevState,
      selectedAgents: selectedAgents,
    }));
  };

  const handleDeletePerspective = async (perspective) => {
    const agents = formData.agentOptions.filter(p => p !== perspective);
    const selectedAgents = formData.selectedAgents.filter(p => p !== perspective);

    setFormData((prevState) => ({
      ...prevState,
      agentOptions: agents,
      selectedAgents: selectedAgents,
    }));

    try {
      const response = await fetch('/api/delete-perspective', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ perspective }),
      });
      const result = await response.json();
    } catch (error) {
      console.error('Error deleting perspective:', error);
    }
  };

  if (!formData || !formData.agentOptions) {
    return <div>No perspectives available.</div>;
  }

  return (
    <div className="perspective-selector-container">
      <div className="agent-box-container">
        {formData.agentOptions.map((perspective, index) => (
          <div
            key={index}
            className={`agent-box ${formData.selectedAgents.includes(perspective) ? 'active' : ''}`}
            onClick={() => handleAgentClick(perspective)}
          >
            {perspective}
            <button
              className="delete-button"
              onClick={(e) => {
                e.stopPropagation();
                handleDeletePerspective(perspective);
              }}
            >
              &times;
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PerspectiveSelector;
