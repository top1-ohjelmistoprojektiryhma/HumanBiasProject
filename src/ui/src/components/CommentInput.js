import React from "react";
import { useState } from "react";

const CommentInput = ({ comment, setComment, showInput, setShowInput }) => {

    return (
        showInput ? (
            <div className="input-form-container">
                <input
                    type="text"
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    placeholder="Enter your comment"
                    className="input-form"
                />
            </div>) : (
            <div className="show-input-button">
                <button onClick={() => setShowInput(true)}>Add Comment</button>
            </div>
        )
    );
}

export default CommentInput;