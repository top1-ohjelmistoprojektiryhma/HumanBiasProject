import React from 'react';

const InputForm = ({ prompt, setPrompt }) => {
  return (
    <div>
      <label>Enter your statement:</label>
      <input 
        type="text" 
        value={prompt} 
        onChange={(e) => setPrompt(e.target.value)} 
      />
    </div>
  );
};

export default InputForm;
