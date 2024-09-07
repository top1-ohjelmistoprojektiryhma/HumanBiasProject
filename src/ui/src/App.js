import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';
import AddPerspectiveForm from './components/AddPerspectiveForm';

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [selectedPerspective, setSelectedPerspective] = useState('');
  const [response, setResponse] = useState('');
  const [perspectives, setPerspectives] = useState([]);

  // Hae agenttien lista backendistä
  useEffect(() => {
    fetch('/api/agents')
      .then((response) => response.json())
      .then((data) => {
        console.log('Fetched agents:', data); // Näyttää haetut agentit
        
        // Tarkista, onko lista tyhjä
        if (data.length === 0) {
          console.log('The agents list is empty.');
        }
  
        setPerspectives(data);  // Asetetaan agentit tilaan
      })
      .catch((error) => console.error('Error fetching agents:', error));
  }, []);
  

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
        perspectives={perspectives}  // Nyt käytämme backendistä haettua dataa
        setSelectedPerspective={setSelectedPerspective} 
      />
      <AddPerspectiveForm perspectives={perspectives} setPerspectives={setPerspectives} />
      <SubmitButton onSubmit={handleSubmit} />
      <ResponseDisplay response={response} />
    </div>
  );
};

export default App;
