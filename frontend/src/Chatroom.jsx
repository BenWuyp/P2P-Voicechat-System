import React, { useEffect, useState } from "react";

const Chatroom = ({
  username,
  chatroomID,
  chatroomName,
  onQuit,
  sendMessage,
  lastMessage,
}) => {
  const [isMuted, setIsMuted] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [enableCam, setEnableCam] = useState(false);
  const [enableVoiceChange, setEnableVoiceChange] = useState(false);
  const [recordedTime, setRecordedTime] = useState("00:00");
  const [recordingList, setRecordingList] = useState([]);
  const [selectedRecording, setSelectedRecording] = useState("");
  const [inputMessage, setInputMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [messageError, setMessageError] = useState("");
  const [users, setUsers] = useState([]);
  const [userCount, setUserCount] = useState(0);

  useEffect(() => {
    let intervalId;

    if (isRecording) {
      let seconds = 0;
      intervalId = setInterval(() => {
        seconds++;
        const minutes = Math.floor(seconds / 60);
        const formattedTime = `${String(minutes).padStart(2, "0")}:${String(
          seconds % 60
        ).padStart(2, "0")}`;
        setRecordedTime(formattedTime);
      }, 1000);
    }

    return () => {
      clearInterval(intervalId);
      setRecordedTime("00:00");
    };
  }, [isRecording]);

  useEffect(() => {
    // Fetch recordings
    if (lastMessage.data[0] !== "{" && lastMessage.data[0] === "[") {
      setRecordingList(JSON.parse(lastMessage.data));
    }
    // Play recording
    if (lastMessage.data[0] !== "{" && lastMessage.data[0] !== "[") {
      const binaryData = Uint8Array.from(atob(lastMessage.data), (c) =>
        c.charCodeAt(0)
      );
      const audioBlob = new Blob([binaryData], { type: "audio/wav" });
      const audioUrl = URL.createObjectURL(audioBlob);

      // Play the audio using the URL
      const audio = new Audio(audioUrl);
      audio.play();
    }
    if (lastMessage.data[0] === "{") {
      try {
        // Chatroom info
        const obj = JSON.parse(lastMessage.data);
        if (obj?.[chatroomName]) {
          setUsers(obj[chatroomName]["members"]);
          setUserCount(obj[chatroomName]["members"].length);
        }
        // Text info
        if (obj?.["textRecords"]) {
          const receivedMessages = obj["textRecords"].map(
            ([sender, content]) => ({
              sender,
              content,
            })
          );
          setMessages(receivedMessages);
        }
      } catch (error) {
        console.log(error);
      }
    }
  }, [lastMessage]);

  useEffect(() => {
    if (isMuted) {
      const jsonStr = JSON.stringify({ action: "mute", payload: true });
      sendMessage(jsonStr);
      const jsonStr2 = JSON.stringify({ action: "terminate_chat_client" });
      sendMessage(jsonStr2);

      console.log("stop");
    } else {
      const jsonStr = JSON.stringify({ action: "mute", payload: false });
      sendMessage(jsonStr);
      const jsonStr2 = JSON.stringify({ action: "run_chat_client" });
      sendMessage(jsonStr2);
      console.log("start");
    }
  }, [isMuted]);

  useEffect(() => {
    const interval = setInterval(() => {
      sendMessage(JSON.stringify({ action: "list", payload: undefined }));
      sendMessage(
        JSON.stringify({ action: "fetch_recordings", payload: undefined })
      );
      sendMessage(
        JSON.stringify({ action: "list_text", payload: chatroomName })
      );
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  const handleRecord = () => {
    setRecorderName(username);
    if (isRecording) {
      sendMessage(JSON.stringify({ action: "end_record", payload: undefined }));
    } else {
      sendMessage(
        JSON.stringify({ action: "start_record", payload: undefined })
      );
    }
    setIsRecording(!isRecording);
  };

  const handleVideo = () => {
    setEnableCam(!enableCam);
  };

  const handleVoiceChange = () => {
    setEnableVoiceChange(!enableVoiceChange);
  };

  const handleRecordingSelect = (event) => {
    setSelectedRecording(event.target.value);
  };

  const handlePlayRecording = () => {
    console.log("Playing recording:", selectedRecording);
    sendMessage(
      JSON.stringify({ action: "fetch_recording", payload: selectedRecording })
    );
  };

  const handleSendMessage = (event) => {
    event.preventDefault();
    if (inputMessage.trim() !== "") {
      // Send message to the chatroom
      sendMessage(
        JSON.stringify({
          action: "store_text",
          payload: {
            chatroom: chatroomName,
            username: username,
            message: inputMessage,
          },
        })
      );

      // Clear the input field
      setInputMessage("");
      setMessageError("");
    } else {
      setMessageError("Message cannot be empty");
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <div className="w-64 bg-indigo-600 w-80 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform -translate-x-full md:translate-x-0 md:inset-0 transition-transform duration-200 ease-in-out bg-indigo-600 text-white p-4">
        <h1 className="text-2xl font-extrabold text-white tracking-tight">
          KK Voice Chat
        </h1>
        <hr></hr>
        <h2 className="text-xl mb-4">Chatroom: {chatroomName}</h2>
        <h2 className="text-xl mb-4">Chatroom Id: {chatroomID}</h2>
        <h2 className="text-xl mb-4">{userCount} Participants</h2>
        <hr></hr>
        <ul>
          {users.map((user, index) => (
            <li key={index} className="mb-2">
              {user}
            </li>
          ))}
        </ul>
        <hr></hr>
        <p>
          <button
            onClick={() => {
              setIsMuted(!isMuted);
            }}
            className="border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700"
          >
            {isMuted ? "🔇" : "🔊"}
          </button>
          <button
            onClick={handleRecord}
            className="border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700"
          >
            {isRecording ? "⏹️" : "⏺"}
          </button>
          <h3>
            {isRecording ? "Recording in Progress" : " "}
            <br></br>
            {isRecording ? `Recorded Time: ${recordedTime}` : " "}
          </h3>
          <form>
            <label>Select a Recording:</label>
            <select
              id="recording"
              name="recording"
              value={selectedRecording}
              onChange={handleRecordingSelect}
              style={{
                marginTop: "10px",
                marginBottom: "10px",
                width: "300px",
              }}
            >
              <option value="">Choose a recording</option>
              {recordingList.map((recording, index) => (
                <option key={index} value={recording}>
                  {recording}
                </option>
              ))}
            </select>
          </form>
          <button
            onClick={handlePlayRecording}
            className="border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700"
            disabled={!selectedRecording}
          >
            Play
          </button>
        </p>
        <hr></hr>
        <button
          onClick={handleVideo}
          className="border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700"
        >
          {enableCam ? "Disable Camera" : "Enable Camera"}
        </button>
        <button
          onClick={handleVoiceChange}
          className="border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700"
        >
          {enableVoiceChange ? "Disable Voice Change" : "Enable Voice Change"}
        </button>
        <hr></hr>
        <p>
          <button
            onClick={onQuit}
            className="border border-white border-3 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700"
          >
            Quit Chatroom
          </button>{" "}
          {/* call onQuit when Quit button is clicked */}
        </p>
      </div>
      <div className="flex-grow p-4">
        {/* Your chatroom content goes here */}
        <div className="p-4 bg-indigo-600 text-white">
          <h2 className="text-xl font-bold">{chatroomName}</h2>
          <p className="text-sm">{userCount} Participants</p>
        </div>

        {/* Chat messages */}
        <div className="flex-grow p-4 overflow-y-auto">
          {messages.map((msg, index) => (
            <div key={index} className="mb-2">
              <span className="font-bold">{msg.sender}: </span>
              <span>{msg.content}</span>
            </div>
          ))}
        </div>

        {/* Chat input */}
        <form className="p-4 border-t">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-indigo-600"
            placeholder="Type your message..."
          />
          <button
            type="submit"
            onClick={handleSendMessage}
            className="mt-2 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700"
          >
            Send
          </button>
          {messageError && (
            <p className="text-red-500 text-sm mt-1">{messageError}</p>
          )}
        </form>
      </div>
    </div>
  );
};

export default Chatroom;
