import React from 'react';

const PasswordInput = ({ password, setPassword }) => {
  return (
    <div className="input-form-container"> 
        <input
          type="password"
          id="secret_password"
          name="secret_password"
          placeholder='Enter password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input-form"
        />
    </div>
  );
};

export default PasswordInput;