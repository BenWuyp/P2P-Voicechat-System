import './App.css';
import React, { useState } from 'react';
import 'tailwindcss/tailwind.css';

const Login = ({ onLogin }) => {
  const [inputUsername, setInputUsername] = useState('Guest');

  const handleLogin = () => {
    onLogin(inputUsername);
  };

  const handleInputChange = (event) => {
    setInputUsername(event.target.value);
  };

  return (
    <div className="h-screen w-screen flex items-center justify-center background py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white bg-opacity-60 rounded-lg p-6">
        <div>
          <h1 className="mt-6 text-center text-4xl font-extrabold text-gray-900">
            KK Voice Chat
          </h1>
          <h2 className="mt-6 text-center text-xl font-extrabold text-gray-900">
            Set a username to start
          </h2>
        </div>
        <div class="flex flex-col space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700">Username</label>
            <input type="text" id="username" name="username" onChange={handleInputChange} className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></input>
          </div>
        </div>
        <button onClick={handleLogin} className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
          Sign In
        </button>
      </div>
    </div>
  );
};

export default Login;
