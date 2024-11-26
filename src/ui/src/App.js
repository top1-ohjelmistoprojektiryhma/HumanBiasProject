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
import PasswordInput from './components/PasswordInput';
import ConfidenceChart from './components/ConfidenceChart';
import FileInput from './components/FileInput';
import SummaryToggle from './components/SummaryToggle';
import BiasChart from './components/BiasChart';


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
  const [showInput, setShowInput] = useState(false);
  const [password, setPassword] = useState(''); // New state for password
  const [isAuthenticated, setIsAuthenticated] = useState(false); // New state for authentication
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
          <button className="submit-button" onClick={handlePasswordSubmit}>Submit password</button>
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
                      {showChart && <ConfidenceChart data={chartData} agents={selectedPerspectives} />}
                      <button onClick={toggleChart}>
                        {showChart ? "Hide Chart" : "Show Chart"}
                      </button>
                      <CommentInput comment={comment} setComment={setComment} showInput={showInput} setShowInput={setShowInput} />
                      <div className='button-group'>
                        <ContinueButton onSubmit={handleContinue} />
                        <StopButton onSubmit={handleStop} />
                        <SummaryButton onClick={handleSummaryClick} />
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