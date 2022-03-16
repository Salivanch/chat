import { Link } from "react-router-dom"

import React, { useState, useEffect, useContext } from "react";

import AuthContext from "../context/AuthContext";

import { useWebSocket } from "../hooks/useWebSocket";
import { useFetch } from "../hooks/useFetch";


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
	const {fetchData} = useFetch("http://127.0.0.1:8000/chats/")
	const [chats, setChats] = useState([])
	const {authTokens} = useContext(AuthContext)
	const socket_url = 'ws://' + '127.0.0.1:8000' + '/ws/chat/' + "?token=" + String(authTokens.access)
	const {data, status, ws} = useWebSocket(socket_url)

	useEffect(() => {
		setChats(fetchData)
	}, [fetchData])

	useEffect(()=>{
		if (status){
			const room_name = data.room_name
			const chat = chats.filter(chat => chat.name == room_name )[0]
			chat.last_message = data.message_data
			setChats(prevChats => ([chat, ...prevChats.filter(item => {
				if (item.id != chat.id) return item
			})]))
		}
	}, [data, ws])

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
