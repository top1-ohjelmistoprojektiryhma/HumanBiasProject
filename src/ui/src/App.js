import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';
import AddPerspectiveForm from './components/AddPerspectiveForm';
import GenerateAgents from './components/GenerateAgents';
import DialogsBar from './components/DialogsBar';
import DialogDisplay from './components/DialogDisplay';
import FormatSelector from './components/FormatSelector';
import ContinueButton from './components/ContinueButton';
import StopButton from './components/StopButton';
import SummaryButton from './components/SummaryButton';

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [selectedPerspectives, setSelectedPerspectives] = useState([]);
  const [perspectives, setPerspectives] = useState([]);
  const [response, setResponse] = useState('');
  const [dialogs, setDialogs] = useState({});
  const [expandedDialogs, setExpandedDialogs] = useState({});
  const [displayedDialog, setDisplayedDialog] = useState(0);
  const [selectedFormat, setSelectedFormat] = useState('dialog');
  const [dialogStarted, setDialogStarted] = useState(false)
  const [summary, setSummary] = useState('');


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
      perspective: selectedPerspectives,
      format: selectedFormat
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
        setDialogStarted(true);
      })
      .catch((error) => {
        console.error('Error processing the statement:', error);
      });
  };

  const handleGenerateAgents = (numAgents) => {
    const requestData = {
      prompt: prompt,
      num_agents: numAgents
    };

    fetch('/api/generate-agents', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((agentResponse) => agentResponse.json())
      .then((data) => {
        if (data.perspectives) {
          setPerspectives(data.perspectives);
        }
      })
      .catch((error) => {
        console.error('Error processing the statement:', error);
      });
  };

  const handleContinue = () => {
    fetch('/api/continue-dialog', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ dialog_id: displayedDialog }),
    })
      .then((response) => response.json())
      .then((data) => {
        const newDialogId = data.dialog_id;
        const newDialog = data.dialog;

        setDialogs((prevState) => ({
          ...prevState,
          [newDialogId]: newDialog
        }));

        setExpandedDialogs({
          [newDialogId]: true
        });

        setDisplayedDialog(newDialogId);
        setResponse("");
      })
      .catch((error) => {
        console.error('Error processing the statement:', error);
      });
  };

  const handleStop = () => {
    setDialogStarted(false);
    setDisplayedDialog(0);
    setResponse("");
    setSelectedPerspectives([]);
    setSelectedFormat("dialog");
  };

  const handleSummaryClick = () => {
    fetch('/api/summary', {
      method: 'GET',  // Change to GET method
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Summary:', data.response);
        setSummary(data.response);
      })
      .catch((error) => {
        console.error('Error sending dialog data:', error);
      });
  };


  return (
    <div className="app-container">
      <DialogsBar dialogs={dialogs} expandedDialogs={expandedDialogs} toggleDialog={setExpandedDialogs} />

      <div className="main-content">
        <h1>Human Bias Project</h1>
        {!dialogStarted && (
          <>
            <InputForm prompt={prompt} setPrompt={setPrompt} />
            <GenerateAgents onSubmit={handleGenerateAgents} />
            <PerspectiveSelector
              perspectives={perspectives}
              selectedPerspectives={selectedPerspectives}
              setSelectedPerspectives={setSelectedPerspectives}
              setPerspectives={setPerspectives}
            />
            <AddPerspectiveForm perspectives={perspectives} setPerspectives={setPerspectives} />
            <FormatSelector setSelectedFormat={setSelectedFormat} />
            <SubmitButton onSubmit={handleSubmit} />
          </>
        )}
        {response && <ResponseDisplay response={response} />}
        {/* Display the dialog content */}
        {displayedDialog !== null && dialogs[displayedDialog] && (
          <>
            <DialogDisplay dialogId={displayedDialog} dialog={dialogs[displayedDialog]} />
            {summary && (
              <div className="summary-section">
                <h2>Summary</h2>
                <p>{summary}</p>
              </div>
            )}
          </>
        )}
        {dialogStarted && <ContinueButton onSubmit={handleContinue} />}
        {dialogStarted && <StopButton onSubmit={handleStop} />}
        {/* Pass the correct dialog data to handleSummaryClick */}
        {dialogStarted && <SummaryButton onClick={handleSummaryClick} />}
      </div>
    </div>
  );
};

export default App;