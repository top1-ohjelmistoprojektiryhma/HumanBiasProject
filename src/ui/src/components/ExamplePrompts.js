import React from 'react';

const ExamplePrompts = ({ setPrompt }) => {
    return (
        <div className="example-prompts">
            <div onClick={() => setPrompt("Finland's education system should be updated for the digital age")}>
                Finland's education system should be updated for the digital age
            </div>
            <div onClick={() => setPrompt("The European Union should invest massively in renewable energy")}>
                The European Union should invest massively in renewable energy
            </div>
            <div onClick={() => setPrompt("Political parties should create a unified strategy to strengthen cybersecurity")}>
                Political parties should create a unified strategy to strengthen cybersecurity
            </div>
        </div>
    );
};

export default ExamplePrompts;
