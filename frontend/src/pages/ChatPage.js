import { useParams } from "react-router-dom"

import React, { useState, useEffect, useContext  } from "react";

import AuthContext from "../context/AuthContext";

import { useWebSocket } from "../hooks/useWebSocket";
import { useFetch } from "../hooks/useFetch";


const MessageList = ({messages}) => {
	return(
		<>
			{messages.map((message) => {
				return(
					<li className="list-group-item" key={message.id}>
                        {message.user?.username} - {message.text} * {message.timestamp}
					</li>
				)
			})}
		</>
	)
}


const MessageForm = ({addMessage}) => {
    const [form, setForm] = useState({"message": ""})

    const handleNameChange = e => {
        const {name, value} = e.target
        setForm(prevForm => ({...prevForm, [name]:value}))
    }

    const handleSubmit = e => {
        e.preventDefault()
        addMessage(form)
        setForm({"message": ""})
    }

    return(
        <form onSubmit={handleSubmit}>
            <div className="row mt-3">
                <div className="col-7 pe-0">
                    <input 
                        type="text" 
                        className="form-control" 
                        id="chat-message-input" 
                        onChange={handleNameChange}
                        name="message"
                        value={form.message}
                    />
                </div>
                <div className="col-5 ps-0">
                    <button 
                        id="chat-message-submit" 
                        type="submit" 
                        className="btn btn-primary"
                    >
                        Send
                    </button>
                </div>
            </div>
        </form>
    )
}


const ChatPage = () => {
	const { authTokens, logoutUser } = useContext(AuthContext);
    const {roomName} = useParams()
    const socket_url = 'ws://' + '127.0.0.1:8000' + '/ws/chat/' + roomName + "/?token=" + String(authTokens.access)
	const { data, status, ws } = useWebSocket(socket_url)
	const [room, setRoom] = useState([]);
	const [messages, setMessages] = useState([]);
	const {fetchData:fetchRooms} = useFetch(`http://127.0.0.1:8000/chats/${roomName}`)
	const {fetchData:fetchMessages} = useFetch(`http://127.0.0.1:8000/chats/${roomName}/messages`)


	useEffect(() => {
		setRoom(fetchRooms)
	}, [fetchRooms]);


	useEffect(() => {
		setMessages(fetchMessages)
	}, [fetchMessages]);


	useEffect(()=>{
        if (status){
            setMessages(prevMessages => ([...prevMessages, data.message]))
        }
	}, [data, ws])

    const sendMessage = form => {
        ws.current.send(JSON.stringify({
            "message": form.message
        }));
    }

	return (
		<div>
			<p>Список сообщений: </p>
			<div className="container">
				<ul className="list-group" id="chat-log">
					{messages && <MessageList messages={messages} />}
				</ul>
                <MessageForm addMessage={sendMessage} />
			</div>
		</div>
	);
};

export default ChatPage;
