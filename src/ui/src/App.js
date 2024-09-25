import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';
import AddPerspectiveForm from './components/AddPerspectiveForm';
import GenerateAgents from './components/GenerateAgents';
import DialogsBar from './components/DialogsBar';
import DialogDisplay from './components/DialogDisplay';

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [selectedPerspectives, setSelectedPerspectives] = useState([]);
  const [perspectives, setPerspectives] = useState([]);
  const [response, setResponse] = useState('');
  const [dialogs, setDialogs] = useState({});
  const [expandedDialogs, setExpandedDialogs] = useState({});
  const [displayedDialog, setDisplayedDialog] = useState(0);

  useEffect(() => {
    fetch('/api/agents')
      .then((response) => response.json())
      .then((data) => {
        setPerspectives(data);
      })
      .catch((error) => console.error('Error fetching agents:', error));

    fetch("/api/all-dialogs")
      .then((response) => response.json())
      .then((data) => {
        setDialogs(data);
      })
      .catch((error) => console.error("Error fetching dialogs:", error));
  }, []);

  const handleSubmit = () => {
    const requestData = {
      prompt: prompt,
      perspective: selectedPerspectives
    };

    fetch('/api/new-dialog', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        const newDialogId = data.dialog_id;
        const newDialog = data.dialog;

        setDialogs((prevState) => ({
          ...prevState,
          [newDialogId]: newDialog
        }));

        setExpandedDialogs((prevState) => ({
          ...prevState,
          [newDialogId]: true
        }));

        setDisplayedDialog(newDialogId);
        setResponse("");
      })
      .catch((error) => {
        console.error('Error processing the statement:', error);
      });
  };

  const handleGenerateAgents = (numAgents) => {
    const requestData = {
      prompt: prompt,
      num_agents: numAgents // Pass the number of agents selected
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
        <GenerateAgents onSubmit={handleGenerateAgents} />
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
