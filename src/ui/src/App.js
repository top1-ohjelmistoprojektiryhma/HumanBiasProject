import React, { useState } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [selectedPerspective, setSelectedPerspective] = useState('');
  const [response, setResponse] = useState('');

  const perspectives = ["farmer", "elderly", "student"];

  const handleSubmit = () => {
    // Mock dataa käytetään tässä vaiheessa, koska backend ei ole vielä valmis
    const mockResponse = `You submitted: "${prompt}" with perspective: "${selectedPerspective}"`;
    setResponse(mockResponse);
  };

  return (
    <div>
      <h1>Human Bias Project</h1>
      <InputForm prompt={prompt} setPrompt={setPrompt} />
      <PerspectiveSelector 
        perspectives={perspectives} 
        setSelectedPerspective={setSelectedPerspective} 
      />
      <SubmitButton onSubmit={handleSubmit} />
      <ResponseDisplay response={response} />
    </div>
  );
};

export default App;
