const BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

export const submitPassword = async (secret_password) => {
    const response = await fetch(`${BASE_URL}/api/submit-password`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ secret_password }),
    });
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}

export const checkIfAuthenticated = async () => {
    const response = await fetch(`${BASE_URL}/api/check-authentication`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}

export const fetchAgents = async () => {
    const response = await fetch(`${BASE_URL}/api/agents`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const fetchDialogs = async () => {
    const response = await fetch(`${BASE_URL}/api/all-sessions`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const fetchFormats = async () => {
    const response = await fetch(`${BASE_URL}/api/formats`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

export const startNewSession = async (requestData) => {
    const response = await fetch(`${BASE_URL}/api/new-session`, {
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
    const response = await fetch(`${BASE_URL}/api/generate-agents`, {
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

export const continueSession = async (sessionId, comment) => {
    const response = await fetch(`${BASE_URL}/api/continue-session`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: sessionId, comment: comment }),
    });
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};