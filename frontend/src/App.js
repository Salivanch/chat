import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import Header from "./components/Header";
import ListChatPage from "./pages/ListChatPage";
import ChatPage from "./pages/ChatPage";

function App() {
  return(
    <BrowserRouter>
      <AuthProvider>
        <Header />
        <Routes>
          <Route exact path="/" element={<PrivateRoute />}>
            <Route exact path="/" element={<HomePage />} />
          </Route>
          <Route exact path="/login" element={<LoginPage />} />
          <Route exact path="/chat" element={<ListChatPage />} />
          <Route exact path="chat/:roomName" element={<ChatPage />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App;
