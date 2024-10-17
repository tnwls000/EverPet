//import { useState } from 'react'
import "./App.css";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import NavBar from "@components/layout/navigation/NavBar/NavBar";
import MainPage from "@components/pages/MainPage";
import MyPage from "@components/pages/MyPage";
import DiaryDetail from "@components/pages/diary/DiaryDetail";
import UserEdit from "./components/pages/mypage/UserEdit";
import RobotEdit from "./components/pages/mypage/RobotEdit";
import axiosInstance from "./api/AxiosInstance";


const useAuth = () => {
  const token = localStorage.getItem("accessToken");
  return { isLoggedIn: !!token };
};

function App() {
  const { isLoggedIn } = useAuth();

  return (
    <>
      <Router>
        <NavBar />
        <Routes>
          <Route
            path="/"
            element={
              isLoggedIn ? <Navigate to="/mypage" replace /> : <MainPage />
            }
          />
          <Route
            path="/mypage/*"
            element={isLoggedIn ? <MyPage /> : <Navigate to="/" replace />}
          />
          <Route path="/user/edit" element={<UserEdit />} />
          <Route path="/robot/edit" element={<RobotEdit />} />
          <Route path="/diary/:id" element={<DiaryDetail />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
