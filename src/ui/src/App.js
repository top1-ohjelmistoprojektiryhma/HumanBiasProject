import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';
import AddPerspectiveForm from './components/AddPerspectiveForm';
import GenerateAgents from './components/GenerateAgents';

/**
 * Main application component.
 * 
 * @component
 */
const App = () => {
  const [prompt, setPrompt] = useState('');
  const [selectedPerspectives, setSelectedPerspectives] = useState([]);
  const [response, setResponse] = useState('');
  const [perspectives, setPerspectives] = useState([]);

  /**
 * Fetch the list of agents from the backend when the component mounts.
 * 
 * @useEffect
 */
  useEffect(() => {
    fetch('/api/agents')
      .then((response) => response.json())
      .then((data) => {
        console.log('Fetched agents:', data); // Display fetched agents

        // Check if the list is empty
        if (data.length === 0) {
          console.log('The agents list is empty.');
        }

        setPerspectives(data);  // Set agents in state
      })
      .catch((error) => console.error('Error fetching agents:', error));
  }, []);

  /**
   * Handle form submission.
   * 
   * Creates an object with the prompt and selected perspectives,
   * sends the data to the Flask backend, and sets the response in the state.
   * 
   * @function
   */
  const handleSubmit = () => {
    // Create an object with the prompt and selected perspectives
    const requestData = {
      prompt: prompt,
      perspective: selectedPerspectives
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

  /**
   * Handle form submission.
   * 
   * Creates an object with the prompt and selected perspectives,
   * sends the data to the Flask backend, and sets the response in the state.
   * 
   * @function
   */
  const handleGenerateAgents = () => {
    // Create an object with the prompt and selected perspectives
    const requestData = {
      prompt: prompt
    };

    // Send the data to the Flask backend
    fetch('/api/generate-agents', {
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
      <GenerateAgents onSubmit={handleGenerateAgents} />
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
