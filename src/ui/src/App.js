import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';
import AddPerspectiveForm from './components/AddPerspectiveForm';
import GenerateAgents from './components/GenerateAgents';
import DialogsBar from "./components/DialogsBar";
import DialogDisplay from './components/DialogDisplay';

/**
 * Main application component.
 * 
 * @component
 */
const App = () => {
  const [prompt, setPrompt] = useState('');
  const [selectedPerspectives, setSelectedPerspectives] = useState([]);
  const [perspectives, setPerspectives] = useState([]);
  const [response, setResponse] = useState('');
  const [dialogs, setDialogs] = useState({});
  const [expandedDialogs, setExpandedDialogs] = useState({});
  const [displayedDialog, setDisplayedDialog] = useState(0);

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

    // Fetch all dialogs from the backend
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

    console.log('Submitting request with data:', requestData);

    fetch('/api/new-dialog', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Received response:', data);
        if (data.response === "Error in processing the prompt") {
          setResponse("Error in processing the prompt");
          return;
        }
        if (data.response === "Please select perspectives") {
          setResponse("Please select perspectives");
          return;
        }

        const newDialogId = data.dialog_id;
        const newDialog = data.dialog;

        setDialogs((prevState) => ({
          ...prevState,
          [newDialogId]: newDialog
        }));

        // Expand the new dialog automatically
        setExpandedDialogs((prevState) => ({
          ...prevState,
          [newDialogId]: true
        }));

        // Set displayed dialog
        setDisplayedDialog(newDialogId);

        // Set response to ""
        setResponse("");
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
      <DialogsBar dialogs={dialogs} expandedDialogs={expandedDialogs} toggleDialog={setExpandedDialogs} />

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
        {response && <ResponseDisplay response={response} />}
        <DialogDisplay dialogId={displayedDialog} dialog={dialogs[displayedDialog]} />
      </div>
    </div>
  );
};

export default App;