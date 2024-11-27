import React from "react";

const ToggleButton = ({ text1, text2, condition, onClick }) => {
    return (
        <button onClick={onClick}>
            {condition ? text1 : text2}
        </button>
    )
}

export default ToggleButton;

