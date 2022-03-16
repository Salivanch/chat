import React, { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const Header = () => {
	const { user, logoutUser } = useContext(AuthContext);

	return (
		<div>
			<div className="d-flex">
				<Link to="/chat">Chats</Link>
				<span> | </span>
				{user ? (
					<a onClick={logoutUser} href="">Logout</a>
				) : (
					<Link to="/login">Login</Link>
				)}
			</div>


			{user && <p>Hello {user.username}</p>}
		</div>
	);
};

export default Header;
