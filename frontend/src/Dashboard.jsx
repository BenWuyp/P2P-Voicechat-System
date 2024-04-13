import React, { useState, useEffect } from "react";
import { Button, TextField, Box, Typography } from "@mui/material";
import { useForm } from "react-hook-form";
import "tailwindcss/tailwind.css";
import userLogo from "./assets/react.svg";

const Dashboard = ({
  username,
  onLogout,
  onJoin,
  sendMessage,
  lastMessage,
}) => {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const [showChatrooms, setShowChatrooms] = useState(false);
  const [showInfo, setShowInfo] = useState(false);
  const [chatroomID, setChatroomID] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [chatrooms, setchatrooms] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      refreshList();
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const onSubmit = (props) => {
    const jsonStr = JSON.stringify({
      action: "create",
      payload: `${props.chatroomName}`,
    });

    sendMessage(jsonStr);
    const chatroom = { name: props.chatroomName, number: 1 };
    const jsonStr2 = JSON.stringify({'action':'run_chat_server'})
    sendMessage(jsonStr2)
    onJoin(chatroom);
  };

  const refreshList = () => {
    const jsonStr = JSON.stringify({ action: "list" });
    sendMessage(jsonStr);
  };

  const handleLogout = () => {
    onLogout();
  };
  const handleChatroomsClick = () => {
    setShowChatrooms(true);
    setShowInfo(false);
  };
  const handleJoinClick = (person) => {
    setChatroomID(person.number);
    onJoin(person);
    const jsonStr = JSON.stringify({
      action: "join",
      payload: `${person.name}`,
    });
    sendMessage(jsonStr);
  };
  // const chatrooms = [
  //   {
  //     name: 'Dummy KK2',
  //     description: 'Opened by KK2',
  //     number: '0',
  //     logo:"data:image/jpeg;base64,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",
  //   },
  // ]

  useEffect(() => {
    if (lastMessage && lastMessage.data) {
      console.log(lastMessage.data);
      const chatrooms = JSON.parse(lastMessage.data);
      let chatroomList = [];
      for (const [name, props] of Object.entries(chatrooms)) {
        const chatroom = {
          name: name,
          number: props.members?.length,
          description: `Created by ${props.createdBy}`,
          logo: "data:image/jpeg;base64,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",
        };
        chatroomList.push(chatroom);
      }
      setchatrooms(chatroomList);
    }
  }, [lastMessage]);

  return (
    <div className="flex bg-gray-50">
      <div className="bg-indigo-600 w-64 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform -translate-x-full md:translate-x-0 md:inset-0 transition-transform duration-200 ease-in-out">
        <h1 className="text-2xl font-extrabold text-white tracking-tight">
          KK Voice Chat
        </h1>
        <hr></hr>
        <nav>
          <a
            onClick={handleChatroomsClick}
            className="block py-2.5 px-4 rounded transition duration-200 bg-indigo-300 hover:bg-indigo-700 hover:text-white"
          >
            Chatrooms
          </a>
          <a
            onClick={handleLogout}
            className="block py-2.5 px-4 rounded transition duration-200 hover: bg-indigo-300 hover:bg-indigo-700 hover:text-white"
          >
            Logout
          </a>
        </nav>
      </div>
      {/* Content area */}
      <div className="h-screen w-screen flex-1 flex flex-col overflow-hidden md:pl-64 transition-all duration-200 ease-in-out">
        <header className="flex-shrink-0 flex items-center justify-between p-2 border-2">
          <div className="flex items-center">
            <img
              src={userLogo}
              alt="User Logo"
              className="h-8 w-8 rounded-full mr-2"
            />
            <span className="mr-2">{username}</span>
          </div>
          <div className="flex w-150">
            <input
              type="text"
              className="flex-grow px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
              placeholder="Search by Room Name"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700">
              Search
            </button>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-2">
          <Box sx={{ margin: "10px" }}>
            <form onSubmit={handleSubmit(onSubmit)}>
              <TextField
                placeholder="chatroom name"
                {...register("chatroomName", { required: true })}
              ></TextField>
              <Button type="submit" variant="contained" sx={{ margin: "10px" }}>
                create chatroom
              </Button>
              {errors.chatroomName && (
                <Typography sx={{ color: "red" }}>
                  This field is required
                </Typography>
              )}
            </form>
          </Box>
          {chatrooms
            .filter((person) =>
              person.name.toLowerCase().includes(searchTerm.toLowerCase())
            )
            .map((person, index) => (
              <ul role="list" className="divide-y divide-gray-100">
                <li
                  key={person.email}
                  className="flex justify-between gap-x-6 py-5"
                >
                  <div className="flex min-w-0 gap-x-4">
                    <img
                      className="h-12 w-12 flex-none rounded-full bg-gray-50"
                      src={person.logo}
                      alt=""
                    />
                    <div className="min-w-0 flex-auto text-left">
                      <p className="text-sm font-semibold leading-6 text-gray-900">
                        {person.name}
                      </p>
                      <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                        {person.description}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-x-4">
                    <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end text-right">
                      <p className="text-sm leading-6 text-gray-900">
                        {person.number} Joined
                      </p>
                      <div className="mt-1 flex items-center gap-x-1.5">
                        <div className="flex-none rounded-full bg-emerald-500/20 p-1">
                          <div className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                        </div>
                        <p className="text-xs leading-5 text-gray-500">
                          Room ID:{index}
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => {
                        handleJoinClick(person);
                      }}
                      className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded hover:bg-green-700"
                    >
                      Join
                    </button>
                  </div>
                </li>
              </ul>
            ))}
        </main>
      </div>
    </div>
  );
};
export default Dashboard;
