import { useParams } from "react-router-dom"

import React, { useState, useEffect, useContext, useRef, useCallback  } from "react";

import AuthContext from "../context/AuthContext";


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


const MessageForm = () => {
    return(
        <form>
            <div className="row mt-3">
                <div className="col-7 pe-0">
                    <input type="text" className="form-control" id="chat-message-input" />
                </div>
                <div className="col-5 ps-0">
                    <button id="chat-message-submit" type="button" className="btn btn-primary">Send</button>
                </div>
            </div>
        </form>
    )
}


const ChatPage = () => {
    const [room, setRoom] = useState([]);
	const [messages, setMessages] = useState([]);
	const { authTokens, logoutUser } = useContext(AuthContext);
	const ws = useRef(null);
    const {roomName} = useParams()

	useEffect(() => {
		getRoom()
        getMessages()

		ws.current = new WebSocket(
			'ws://'
			+ '127.0.0.1:8000'
			+ '/ws/chat/'
            + roomName
			+ "/?token=" + String(authTokens.access)
		)

		ws.current.onopen = () => console.log("Соединение открыто");
		ws.current.onclose = () => console.log("Соединение закрыто");

		gettingData();
	}, []);


	const gettingData = useCallback(() => {
		if (!ws.current) return;

		ws.current.onmessage = e => {
			const message = JSON.parse(e.data);
			console.log(message)
		};
	}, [] )

	const getRoom = async () => {
		const response = await fetch(`http://127.0.0.1:8000/chats/${roomName}/messages`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: "Bearer " + String(authTokens.access),
			},
		});

		const data = await response.json();

		if (response.status === 200) {
            setMessages(data)
            console.log(data)
		} else if (response.statusText === "Unauthorized") {
			logoutUser();
			console.log("Не пускает")
		}
	};

    const getMessages = async () => {
		const response = await fetch(`http://127.0.0.1:8000/chats/${roomName}`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: "Bearer " + String(authTokens.access),
			},
		});

		const data = await response.json();

		if (response.status === 200) {
            setRoom(data)
            console.log(data)
		} else if (response.statusText === "Unauthorized") {
			logoutUser();
			console.log("Не пускает")
		}
	};

    if (document.querySelector('#chat-message-input')){
        ws.current.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log(data)
            let liLast = document.createElement('li');
            liLast.className = "list-group-item";
            liLast.innerHTML = `${data.message.user} - ${data.message.text} * ${data.message.timestamp}`;
            document.querySelector('#chat-log').append(liLast);;
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };
    
        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            ws.current.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
    }

	return (
		<div>
			<p>Список сообщений: </p>
			<div className="container">
				<ul className="list-group" id="chat-log">
					{messages && <MessageList messages={messages} />}
				</ul>
                <MessageForm />
			</div>
		</div>
	);
};

export default ChatPage;
