import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm.jsx';
import PerspectiveSelector from './components/PerspectiveSelector.jsx';
import ResponseDisplay from './components/ResponseDisplay.jsx';
import GenerateAgents from './components/GenerateAgents.jsx';
import DialogsBar from './components/DialogsBar.jsx';
import DialogDisplay from './components/DialogDisplay.jsx';
import FormatSelector from './components/FormatSelector.jsx';
import ExamplePrompts from './components/ExamplePrompts.jsx';
import CommentInput from './components/CommentInput.jsx';
import PasswordInput from './components/PasswordInput.jsx';
import FileInput from './components/FileInput.jsx';
import SummaryToggle from './components/SummaryToggle.jsx';
import ConfidenceChart from './components/ConfidenceChart.jsx';
import BiasChart from './components/BiasChart.jsx';
import Button from './components/common/Button.jsx';
import ToggleButton from './components/common/ToggleButton.jsx';

import {
  fetchAgents,
  fetchDialogs,
  fetchFormats,
  startNewSession,
  generateAgents,
  continueSession,
  submitPassword,
  checkIfAuthenticated,
  readFile,
  fetchSummary,
} from './api.js';

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
  const [isDialogsBarVisible, setIsDialogsBarVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [comment, setComment] = useState('');
  const [showInput, setShowInput] = useState(false);
  const [password, setPassword] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [chartData, setChartData] = useState({});
  const [showChart, setShowChart] = useState(false);
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [summaryEnabled, setSummaryEnabled] = useState(false);
  const [biasData, setBiasData] = useState({})


  const handlePasswordSubmit = async () => {
    try {
      await submitPassword(password);
      setIsAuthenticated(true);
      localStorage.setItem('isAuthenticated', 'true');
      setError('');
    } catch (error) {
      console.error('Error submitting password:', error);
      setError('Incorrect password');
    }
  };

  // Check if the user is already authenticated
  useEffect(() => {
    const checkAuthStatus = async () => {
      const storedAuth = localStorage.getItem('isAuthenticated');
      setIsAuthenticated(storedAuth === 'true');
      if (storedAuth === 'true') {
        try {
          const response = await checkIfAuthenticated();
          if (response.authenticated) {
            setIsAuthenticated(true);
          } else {
            localStorage.removeItem('isAuthenticated');
            setIsAuthenticated(false);
          }
        } catch (error) {
          console.error('Error checking session:', error);
          localStorage.removeItem('isAuthenticated');
        }
      }
    };

    checkAuthStatus();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const agentsData = await fetchAgents();
        setPerspectives(agentsData);

        const dialogsData = await fetchDialogs();
        setDialogs(dialogsData);

        const formatsData = await fetchFormats();
        setFormatOptions(formatsData);
        setSelectedFormat(formatsData[0]);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    if (isAuthenticated || process.env.NODE_ENV === 'development') {
      fetchData();
    }
  }, [isAuthenticated]);

  const validateUserInput = () => {
    if (selectedPerspectives.length === 0) {
      setError('Please select at least one perspective.');
      return false;
    }
    if (prompt === '' && !file) {
      setError('Please enter a statement.');
      return false;
    }
    setError('');
    return true;
  };

  const collectScores = (newDialog) => {
    const scores = {};
    const rounds = newDialog['rounds'];
    const agents = new Set();

    // Collect all agent roles
    for (const round in rounds) {
      if (Array.isArray(rounds[round])) {
        rounds[round].forEach(entry => {
          if (entry.agent) {
            agents.add(entry.agent);
          }
        });
      }
    }

    // Initialize scores for each agent
    agents.forEach(agent => {
      scores[agent] = [];
    });

    // Populate scores with actual data or null
    for (const round in rounds) {
      const roundNumber = parseInt(round, 10);
      if (Array.isArray(rounds[round])) {
        const roundScores = {};
        rounds[round].forEach(entry => {
          const agent_role = entry.agent;
          const conf_score = entry.conf_score;
          const score_summary = entry.score_summary;
          if (agent_role !== undefined && conf_score !== undefined) {
            roundScores[agent_role] = [`"${score_summary}"`, conf_score, roundNumber];
          } else {
            console.warn(`Missing agent_role or conf_score in entry:`, entry);
          }
        });

        // Ensure each agent has a response for this round
        agents.forEach(agent => {
          if (roundScores[agent]) {
            scores[agent].push(roundScores[agent]);
          } else {
            scores[agent].push([null, null, roundNumber]);
          }
        });
      } else {
        console.warn(`Expected an array for round ${round}, but got:`, newDialog[round]);
      }
    }

    return scores;
  };

  const handleSubmit = async () => {
    setLoading(true)
    let promptContent = prompt;
    if (file) {
      const data = await readFile(file);
      promptContent = data.response;
    }
    if (!validateUserInput()) {
      setLoading(false)
      return;
    }
    setDisplayedSession(null);
    setSummary('');
    const requestData = {
      prompt: promptContent,
      perspective: selectedPerspectives,
      format: selectedFormat,
      summaryEnabled,
    };

    try {
      const data = await startNewSession(requestData);
      const newSessionId = data.session_id;
      const newDialog = data.dialog;

      const scores = collectScores(newDialog, chartData);
      setChartData(scores);

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
    setLoading(true);
    if (prompt === '' && !file) {
      setError('Please enter a statement.');
      setLoading(false);
      return false;
    }
    let promptContent = prompt;
    if (file) {
      const allowedExtensions = [".txt", ".pdf", ".docx", ".odt"];
      const fileExtension = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();

      if (!allowedExtensions.includes(fileExtension)) {
        setError("Invalid file type");
        console.error("Invalid file type");
        return;
      }
      promptContent = await readFile(file);
    }
    const requestData = {
      prompt: promptContent,
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
    setLoading(false);
  };
  const handleContinue = async () => {
    setLoading(true);
    try {
      const data = await continueSession(displayedSession, comment);
      const newSessionId = data.session_id;
      const newDialog = data.dialog;
      const scores = collectScores(newDialog, chartData);
      setChartData(scores);

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
      setShowInput(false);
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
    setFile(null);
    setFileName('');
  };

  const handleSummaryClick = async () => {
    setLoading(true);
    try {
      const data = await fetchSummary();
      setSummary(data.response[0]);
      setBiases(data.response[1]);
      setBiasData(data.response[2]);
    } catch (error) {
      console.error('Error sending dialog data:', error);
    }
    setLoading(false);
  };

  const handleToggleDialogsBar = () => {
    setIsDialogsBarVisible(!isDialogsBarVisible);
    if (!isDialogsBarVisible) {
      document.body.classList.add('dialogs-bar-open');
    } else {
      document.body.classList.remove('dialogs-bar-open');
    }
  };

  const toggleChart = () => {
    setShowChart((prevShowChart) => !prevShowChart);
  };


  return (
    <div className="app-container">
      {!isAuthenticated && process.env.NODE_ENV !== 'development' ? (
        <div className="password-container">
          <PasswordInput
            password={password}
            setPassword={setPassword}
          />
          <Button text="Submit password" onClick={handlePasswordSubmit} />
          {error && <div className="error-message">{error}</div>}
        </div>
      ) : (
        <>
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

            {!dialogStarted && (
              <>
                <ExamplePrompts setPrompt={setPrompt} />
                <InputForm prompt={prompt} setPrompt={setPrompt} />
              </>
            )}


            {!dialogStarted && (
              <div className="file-drop-container">
                <FileInput setFile={setFile} />
              </div>
            )}

            {/* centered-column alkaa tästä */}
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
                  <SummaryToggle
                    summaryEnabled={summaryEnabled}
                    setSummaryEnabled={setSummaryEnabled}
                  />
                  <FormatSelector formatOptions={formatOptions} setSelectedFormat={setSelectedFormat} />
                  <Button text="Submit" onClick={handleSubmit} />
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
                      {showChart && <ConfidenceChart data={chartData} agents={selectedPerspectives} />}
                      <ToggleButton text1="Hide Chart" text2="Show Chart" condition={showChart} onClick={toggleChart} />
                      <CommentInput comment={comment} setComment={setComment} showInput={showInput} setShowInput={setShowInput} />
                      <div className='button-group'>
                        <Button text="Continue" onClick={handleContinue} />
                        <Button text="Stop" onClick={handleStop} />
                        <Button text="Show Summary" onClick={handleSummaryClick} />
                        {summary && (
                          <div className="summary-section">
                            <BiasChart data={biasData} />
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
        </>
      )}
    </div>
  );
};

export default App;