export const fetchAgents = async () => {
    const response = await fetch('/api/agents');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const fetchDialogs = async () => {
    const response = await fetch('/api/all-sessions');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const fetchFormats = async () => {
    const response = await fetch('/api/formats');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const startNewSession = async (requestData) => {
    const response = await fetch('/api/new-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    });
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const generateAgents = async (requestData) => {
    const response = await fetch('/api/generate-agents', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    });
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const continueSession = async (sessionId) => {
    const response = await fetch('/api/continue-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: sessionId }),
    });
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};