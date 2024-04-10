import React, { useState } from 'react';
import Login from './Login';
import Dashboard from './Dashboard';
import Chatroom from './Chatroom'; 

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [isJoinedIn, setIsJoinedIn] = useState(false);
  const [chatroom, setChatroom] = useState(null);

  const handleLogin = (username) => {
    setIsLoggedIn(true);
    setUsername(username);
    setIsJoinedIn(false);
    setChatroom(null);
  };

  const handleLogout = () => {
    setIsJoinedIn(false);
    setIsLoggedIn(false);
    setUsername('');
    setChatroom(null);
  };

  const handleJoin = (chatroom) => {
    setIsLoggedIn(true);
    setIsJoinedIn(true);
    setChatroom(chatroom);
  };

  const handleQuitChat = () => {
    setIsJoinedIn(false);
    setIsLoggedIn(true);
    setChatroom(null);
    setRecorderName("None");
  };

  return (
    <div className="App">
      {isLoggedIn ? (
        isJoinedIn ? (
          <Chatroom username={username} chatroomID={chatroom.number} chatroomName={chatroom.name} onQuit={handleQuitChat} />
        ) : (
          <Dashboard username={username} onLogout={handleLogout} onJoin={handleJoin} />
        )
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
