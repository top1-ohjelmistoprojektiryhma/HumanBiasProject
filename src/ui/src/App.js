import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';
import AddPerspectiveForm from './components/AddPerspectiveForm';

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [selectedPerspectives, setSelectedPerspectives] = useState([]);
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
    // Create an object with the prompt and selected perspectives
    const requestData = {
      prompt: prompt,
      perspective: selectedPerspectives.length > 0 ? selectedPerspectives[0] : null, // sending only the first selected perspective for simplicity
    };
  
    // Send the data to the Flask backend
    fetch('/api/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),  // Convert the data to JSON
    })
      .then((response) => response.json())
      .then((data) => {
        // Set the response from the backend in the state
        setResponse(data.response);
      })
      .catch((error) => {
        console.error('Error processing the statement:', error);
      });
  };
  

  return (
    <div>
      <h1>Human Bias Project</h1>
      <InputForm prompt={prompt} setPrompt={setPrompt} />
      <PerspectiveSelector 
        perspectives={perspectives} 
        selectedPerspectives={selectedPerspectives} 
        setSelectedPerspectives={setSelectedPerspectives} 
        setPerspectives={setPerspectives} 
      />
      <AddPerspectiveForm perspectives={perspectives} setPerspectives={setPerspectives} />
      <SubmitButton onSubmit={handleSubmit} />
      <ResponseDisplay response={response} />
    </div>
  );
};

export default App;
