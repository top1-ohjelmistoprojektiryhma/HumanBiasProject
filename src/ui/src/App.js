import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';
import AddPerspectiveForm from './components/AddPerspectiveForm';
import GenerateAgents from './components/GenerateAgents';
import DialogsBar from "./components/DialogsBar"; // Import dialogs bar

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
  const [dialogs, setDialogs] = useState([]); // Tila dialogeille
  const [expandedDialogs, setExpandedDialogs] = useState({}); // Tila laajennetuille dialogeille

  /**
   * Fetch the list of agents from the backend when the component mounts.
   */
  useEffect(() => {
    fetch('/api/agents')
      .then((response) => response.json())
      .then((data) => {
        console.log('Fetched agents:', data);
        if (data.length === 0) {
          console.log('The agents list is empty.');
        }
        setPerspectives(data);
      })
      .catch((error) => console.error('Error fetching agents:', error));

    // Haetaan dialogit heti kun komponentti ladataan
    fetch("/api/all-dialogs")
      .then((response) => response.json())
      .then((data) => {
        setDialogs(data);
      })
      .catch((error) => console.error("Error fetching dialogs:", error));
  }, []);

  /**
   * Handle form submission for a new prompt.
   */
  const handleSubmit = () => {
    const requestData = {
      prompt: prompt,
      perspective: selectedPerspectives
    };

    fetch('/api/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        setResponse(data.response);
        
        // Luo uusi dialogi täydellisellä rakenteella ja lisää sen tilaan
        const newDialogId = Object.keys(dialogs).length; // Uusi dialogin ID
        const newDialog = {
          [newDialogId]: {
            initial_prompt: prompt,
            rounds: {} // Tyhjä rounds-rakenne
          }
        };
        
        // Päivitetään dialogs-tila
        setDialogs((prevDialogs) => ({
          ...prevDialogs,
          ...newDialog
        }));
  
        // Avaa uusi dialogi automaattisesti
        setExpandedDialogs((prevState) => ({
          ...prevState,
          [newDialogId]: true
        }));
      })
      .catch((error) => {
        console.error('Error processing the statement:', error);
      });
  };

  /**
   * Handle form submission for generating agents.
   */
  const handleGenerateAgents = () => {
    const requestData = {
      prompt: prompt
    };

    fetch('/api/generate-agents', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.perspectives) {
          setPerspectives(data.perspectives);
        } else {
          console.error('Error generating agents:', data.error);
        }
        setResponse(data.response);
      })
      .catch((error) => {
        console.error('Error processing the statement:', error);
      });
  };

  return (
    <div className="app-container">
      <DialogsBar dialogs={dialogs} expandedDialogs={expandedDialogs} toggleDialog={setExpandedDialogs} /> {/* Pass dialogs and expanded state */}

      <div className="main-content">
        <h1>Human Bias Project</h1>
        <InputForm prompt={prompt} setPrompt={setPrompt} />
        <GenerateAgents onSubmit={handleGenerateAgents} perspectives={perspectives} setPerspectives={setPerspectives} />
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
    </div>
  );
};

export default App;


