import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import PerspectiveSelector from './components/PerspectiveSelector';
import SubmitButton from './components/SubmitButton';
import ResponseDisplay from './components/ResponseDisplay';
import GenerateAgents from './components/GenerateAgents';
import DialogsBar from './components/DialogsBar';
import DialogDisplay from './components/DialogDisplay';
import FormatSelector from './components/FormatSelector';
import ContinueButton from './components/ContinueButton';
import StopButton from './components/StopButton';
import SummaryButton from './components/SummaryButton';
import ExamplePrompts from './components/ExamplePrompts';
import CommentInput from './components/CommentInput';
import {
  fetchAgents,
  fetchDialogs,
  fetchFormats,
  startNewSession,
  generateAgents,
  continueSession,
} from './api';


const App = () => {
  const [prompt, setPrompt] = useState('');
  const [selectedPerspectives, setSelectedPerspectives] = useState([]);
  const [perspectives, setPerspectives] = useState([]);
  const [response, setResponse] = useState('');
  const [dialogs, setDialogs] = useState({});
  const [expandedDialogs, setExpandedDialogs] = useState({});
  const [displayedSession, setDisplayedSession] = useState(0);
  const [selectedFormat, setSelectedFormat] = useState('');
  const [dialogStarted, setDialogStarted] = useState(false)
  const [summary, setSummary] = useState('');
  const [biases, setBiases] = useState('');
  const [error, setError] = useState("");
  const [formatOptions, setFormatOptions] = useState([]);
  const [isDialogsBarVisible, setIsDialogsBarVisible] = useState(false); // New state for visibility
  const [loading, setLoading] = useState(false);
  const [comment, setComment] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const agentsData = await fetchAgents();
        setPerspectives(agentsData);

        const dialogsData = await fetchDialogs();
        setDialogs(dialogsData);

        const formatsData = await fetchFormats();
        setFormatOptions(formatsData);
        setSelectedFormat(formatsData[0])
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const validateUserInput = () => {
    if (selectedPerspectives.length === 0) {
      setError('Please select at least one perspective.');
      return false;
    }
    if (prompt === '') {
      setError('Please enter a statement.');
      return false;
    }
    setError('');
    return true;
  };

  const handleSubmit = async () => {
    if (!validateUserInput()) {
      return;
    }
    setDisplayedSession(null);
    setSummary('');
    setLoading(true);

    const requestData = {
      prompt: prompt,
      perspective: selectedPerspectives,
      format: selectedFormat,
    };

    try {
      const data = await startNewSession(requestData);
      const newSessionId = data.session_id;
      const newDialog = data.dialog;

      setDialogs((prevState) => ({
        ...prevState,
        [newSessionId]: newDialog,
      }));

      setExpandedDialogs((prevState) => ({
        ...prevState,
        [newSessionId]: true,
      }));

      setDisplayedSession(newSessionId);
      setResponse('');
      setDialogStarted(true);
    } catch (error) {
      console.error('Error processing the statement:', error);
    }
    setLoading(false);
    setPrompt('');
  };
  const handleGenerateAgents = async (numAgents) => {
    const requestData = {
      prompt: prompt,
      num_agents: numAgents,
    };

    try {
      const data = await generateAgents(requestData);
      if (data.perspectives) {
        setPerspectives(data.perspectives);
      }
    } catch (error) {
      console.error('Error generating agents:', error);
    }
  };
  const handleContinue = async () => {
    console.log(comment)
    setLoading(true);
    try {
      const data = await continueSession(displayedSession, comment);
      const newSessionId = data.session_id;
      const newDialog = data.dialog;

      setDialogs((prevState) => ({
        ...prevState,
        [newSessionId]: newDialog
      }));

      setExpandedDialogs({
        [newSessionId]: true
      });

      setDisplayedSession(newSessionId);
      setResponse("");
      setComment("");
    } catch (error) {
      console.error('Error continuing the dialog:', error);
    }
    setLoading(false);
  };

  const handleStop = () => {
    setDialogStarted(false);
    setDisplayedSession(0);
    setResponse("");
    setSelectedPerspectives([]);
    setSelectedFormat(formatOptions[0]);
    setPrompt('');
  };

  const handleSummaryClick = () => {
    fetch('/api/summary', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Summary:', data.response);
        setSummary(data.response[0]); // summary index in array
        setBiases(data.response[1]); // biases index in array
      })
      .catch((error) => {
        console.error('Error sending dialog data:', error);
      });
  };
  const handleToggleDialogsBar = () => {
    setIsDialogsBarVisible(!isDialogsBarVisible);
  };



  return (
    <div className="app-container">
      <div className="menu-symbol" onClick={handleToggleDialogsBar}>
        &#9776; {/* Unicode character for the menu symbol */}
      </div>

      <div className={`dialogs-bar ${isDialogsBarVisible ? '' : 'dialogs-bar-hidden'}`}>
        <DialogsBar
          dialogs={dialogs}
          expandedDialogs={expandedDialogs}
          toggleDialog={setExpandedDialogs}
        />
      </div>

      <div className={`main-content ${isDialogsBarVisible ? 'main-content-shift' : ''}`}>
        <h1>Human Bias Project</h1>
        {!dialogStarted && (
          <>
            <ExamplePrompts setPrompt={setPrompt} />
            <InputForm prompt={prompt} setPrompt={setPrompt} />
          </>
        )}
        <div className="centered-column">
          {!dialogStarted && (
            <>
              <div className="generate-agents-container">
                <GenerateAgents
                  perspectives={perspectives}
                  setPerspectives={setPerspectives}
                  onSubmit={handleGenerateAgents}
                />
              </div>

              <PerspectiveSelector
                perspectives={perspectives}
                selectedPerspectives={selectedPerspectives}
                setSelectedPerspectives={setSelectedPerspectives}
                setPerspectives={setPerspectives}
              />
              <FormatSelector formatOptions={formatOptions} setSelectedFormat={setSelectedFormat} />
              <SubmitButton onSubmit={handleSubmit} />
              {loading ? (
                <div className="spinner-container">
                  <div className="spinner"></div>
                </div>
              ) : null}
              {error && <div className="error-message">{error}</div>}
            </>
          )}

          {response && <ResponseDisplay response={response} />}
          {displayedSession !== null && dialogs[displayedSession] && (
            <>
              <DialogDisplay dialogId={displayedSession} dialog={dialogs[displayedSession]} />
              {loading ? (
                <div className="spinner-container">
                  <div className="spinner"></div>
                </div>
              ) : null}
              {dialogStarted && (
                <>
                  {selectedFormat === "dialog - user comments" && <CommentInput comment={comment} setComment={setComment} />}
                  <div className='button-group'>
                    <ContinueButton onSubmit={handleContinue} />
                    <StopButton onSubmit={handleStop} />
                    <SummaryButton onClick={handleSummaryClick} />
                    {summary && (
                      <div className="summary-section">
                        <h2>Summary</h2>
                        <p>{summary}</p>
                        <h2>Biases</h2>
                        <p>{biases}</p>
                      </div>
                    )}
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
