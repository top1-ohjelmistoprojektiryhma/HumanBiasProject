import React from 'react';

const SummaryButton = ({ onClick }) => {
    return (
        <button onClick={onClick}>
            Show Summary
        </button>
    );
};

export default SummaryButton;