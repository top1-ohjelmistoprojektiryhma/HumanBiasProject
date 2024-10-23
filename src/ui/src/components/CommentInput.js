import React from "react";

const CommentInput = ({ comment, setComment }) => {
    return (
        <div className="input-form-container">
            <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Enter your comment"
                className="input-form"
            />
        </div>
    );
}

export default CommentInput;