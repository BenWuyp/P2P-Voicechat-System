import React, { useState, useEffect } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

import Login from "./Login";
import Dashboard from "./Dashboard";
import Chatroom from "./Chatroom";

const WS_URL = "ws://127.0.0.1:8765";

function App() {
  const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL, {
    onOpen: () => {
      console.log("WebSocket connection established.");
    },
    onClose: () => {
      const jsonStr = JSON.stringify({ action: "terminate_chat_client" });
      sendMessage(jsonStr);
    },
  });

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [isJoinedIn, setIsJoinedIn] = useState(false);
  const [chatroom, setChatroom] = useState(null);

  const handleLogin = (username) => {
    setIsLoggedIn(true);
    setUsername(username);
    setIsJoinedIn(false);
    setChatroom(null);
    sendMessage(username);
  };

  const handleLogout = () => {
    setIsJoinedIn(false);
    setIsLoggedIn(false);
    setUsername("");
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

    const jsonStr = JSON.stringify({
      action: "quit",
      payload: `${chatroom.name}`,
    });
    sendMessage(jsonStr);

    const jsonStr2 = JSON.stringify({
      action: "terminate_chat_client",
    });
    sendMessage(jsonStr2);

    const jsonStr3 = JSON.stringify({
      action: "terminate_chat_server",
    });
    sendMessage(jsonStr3);

    setChatroom(null);
    setRecorderName("None");
  };

  return (
    <div className="App">
      {isLoggedIn ? (
        isJoinedIn ? (
          <Chatroom
            username={username}
            chatroomID={chatroom.number}
            chatroomName={chatroom.name}
            onQuit={handleQuitChat}
            sendMessage={sendMessage}
            lastMessage={lastMessage}
          />
        ) : (
          <Dashboard
            username={username}
            onLogout={handleLogout}
            onJoin={handleJoin}
            sendMessage={sendMessage}
            lastMessage={lastMessage}
          />
        )
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
