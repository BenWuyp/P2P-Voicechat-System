import React, { useEffect, useState } from 'react';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  let socket;

  useEffect(() => {
    // Create WebSocket connection.
    socket = new WebSocket('ws://localhost:8765');

    // Connection opened
    socket.addEventListener('open', (event) => {
      socket.send('Hello Server!');
    });

    // Listen for messages
    socket.addEventListener('message', (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    });

    // Connection closed
    socket.addEventListener('close', (event) => {
      console.log('Connection closed');
    });

    // Connection error
    socket.addEventListener('error', (event) => {
      console.log('Connection error');
    });

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div>
      <h1>Messages</h1>
      {messages.map((message, index) => (
        <p key={index}>{message}</p>
      ))}
    </div>
  );
};

export default ChatPage;
