import { Link } from "react-router-dom"

import React, { useState, useEffect, useContext, useRef, useCallback  } from "react";

import AuthContext from "../context/AuthContext";


const ChatList = ({chats}) => {
	return(
		<>
			{chats.map((chat) => {
				return(
					<li className="list-group-item" key={chat.name}>
						<Link to={chat.name}>{chat.name}</Link>
						<p className="text">
							{chat.last_message.text}
						</p>
					</li>
				)
			})}
		</>
	)
}


const ListChatPage = () => {
	const [chats, setChats] = useState([]);
	const { authTokens, logoutUser } = useContext(AuthContext);
	const ws = useRef(null);

	useEffect(() => {
		getChats()
		
		ws.current = new WebSocket(
			'ws://'
			+ '127.0.0.1:8000'
			+ '/ws/chat/'
			+ "?token=" + String(authTokens.access)
		)

		ws.current.onopen = () => console.log("Соединение открыто");
		ws.current.onclose = () => console.log("Соединение закрыто");

		gettingData();
	}, []);

	const test = () => {
		console.log(chats)
	}

	test()

	const gettingData = useCallback(() => {
		if (!ws.current) return;

		ws.current.onmessage = e => {
			test()
			const message = JSON.parse(e.data);
			const message_data = message.message_data
			const room_name = message.room_name

			// const chat = chats.filter(chat => chat.name == room_name )
			// console.log(chats)
			// console.log(authTokens)

		};
	}, [] )

	const getChats = async () => {
		const response = await fetch("http://127.0.0.1:8000/chats/", {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: "Bearer " + String(authTokens.access),
			},
		});

		const data = await response.json();

		if (response.status === 200) {
			setChats(data);
			// console.log(data)
		} else if (response.statusText === "Unauthorized") {
			logoutUser();
			console.log("Не пускает")
		}
	};

	return (
		<div>
			<p>Список чатов: </p>
			<div className="container">
				<ul className="list-group" id="chat-log">
					{chats && <ChatList chats={chats} />}
				</ul>
			</div>
		</div>
	);
};

export default ListChatPage;
