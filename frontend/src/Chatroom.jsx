import React, { useState, useEffect } from "react";
import "tailwindcss/tailwind.css";

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
  const [RecorderName, setRecorderName] = useState(false);
  const [enableCam, setEnableCam] = useState(false);
  const [enableVoiceChange, setEnableVoiceChange] = useState(false);
  const [recordedTime, setRecordedTime] = useState("00:00");
  const [recordingList, setRecordingList] = useState([]);
  const [selectedRecording, setSelectedRecording] = useState("");

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
    if (lastMessage.data[0] !== "{") {
      setRecordingList(JSON.parse(lastMessage.data));
    }
  }, [lastMessage]);

  const handleMute = () => {
    setIsMuted((prevMuteStatus) => {
      const newMuteStatus = !prevMuteStatus;
      sendMessage(JSON.stringify({ action: "mute", payload: newMuteStatus }));
      return newMuteStatus;
    });
  };

  const handleRecord = () => {
    setRecorderName(username);
    if (isRecording) {
      sendMessage(JSON.stringify({ action: "end_record", payload: undefined }));
    } else {
      sendMessage(
        JSON.stringify({ action: "start_record", payload: undefined })
      );
    }
    sendMessage(
      JSON.stringify({ action: "fetch_recordings", payload: undefined })
    );
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
    // Implement logic to play the selected recording
    console.log("Playing recording:", selectedRecording);
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
        <h2 className="text-xl mb-4">{chatroomID} Participants</h2>
        <hr></hr>
        <ul>
          <li className="mb-2">participant 1</li>
          <li className="mb-2">participant 2</li>
          <li className="mb-2">participant 3</li>
        </ul>
        <hr></hr>
        <p>
          <button
            onClick={handleMute}
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
        <table className="w-screen h-screen">
          <tr>
            <th className="border-4 border-green-500 ">User1</th>
            <th className="border-4 border-green-500">User2</th>
          </tr>
          <tr>
            <td className="border-4 border-green-500">User4</td>
            <td className="border-4 border-green-500">User99</td>
          </tr>
        </table>
      </div>
    </div>
  );
};

export default Chatroom;
