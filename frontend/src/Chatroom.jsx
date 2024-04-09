import React, { useState } from 'react';
import 'tailwindcss/tailwind.css';

const Chatroom = ({ username, chatroomID, chatroomName, onQuit }) => {
    const [isMuted, setIsMuted] = useState(false);
    const [isRecording, setIsRecording] = useState(false);
    const [RecorderName, setRecorderName] = useState(false);
    const handleMute = () => {
        setIsMuted(!isMuted);
    }

    const handleRecord = () => {
        setRecorderName(username);
        setIsRecording(!isRecording);
    }

    return(
        <div className="flex flex-col min-h-screen">
          <div className="w-64bg-indigo-600 w-80 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform -translate-x-full md:translate-x-0 md:inset-0 transition-transform duration-200 ease-in-out bg-indigo-600 text-white p-4">
            <h1 className="text-2xl font-extrabold text-white tracking-tight">KK Voice Chat</h1>
            <hr></hr>
            <h2 className="text-xl mb-4">{chatroomName}'s Chatroom</h2>
            <h2 className="text-xl mb-4">Chatroom Id: {chatroomID}</h2>
            <h2 className="text-xl mb-4">No. Participants</h2>
            <hr></hr>
            <ul>
              <li className="mb-2">Participant Name 1</li>
              <li className="mb-2">Participant Name 2</li>
              <li className="mb-2">Participant Name 99</li>
            </ul>
            <hr></hr>
            <p>
              <button onClick={handleMute} className='border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700'>{isMuted ? '🔇' : '🔊'}</button>
              <button onClick={handleRecord} className='border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700'>{isRecording ? '⏹️' : '⏺'}</button>
              <h3>{isRecording ? 'Recording in Progress' : ' '}<br></br>{isRecording ? 'Recorded Time: mm:ss':' '}</h3>
            </p>
            <hr></hr>
            <p>
              <button onClick={onQuit} className='border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700'>Quit Chatroom</button> {/* call onQuit when Quit button is clicked */}
            </p>
          </div>
          <div className="flex-grow p-4">
            {/* Your chatroom content goes here */}
          </div>
        </div>
      );
    }
    
    export default Chatroom;
