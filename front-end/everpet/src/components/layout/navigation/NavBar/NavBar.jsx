import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios"; // axios 임포트
import "bootstrap/dist/css/bootstrap.min.css";
import { Navbar, Container, Nav, Button } from "react-bootstrap";
import "@/css/button/Button.css";
import SignUpModal from "../../../popups/auth/SignUpModal";
import SignInModal from "../../../popups/auth/SignInModal";
import FindIdModal from "../../../popups/auth/FindIdModal";
import FindPasswordModal from "../../../popups/auth/FindPasswordModal";
import axiosInstance from "@/api/AxiosInstance.js";

function NavBar() {
  const [signUpModalOn, setsignUpModalOn] = useState(false);
  const [signInModalOn, setSignInModalOn] = useState(false);
  const [findIdModalOn, setFindIdModalOn] = useState(false);
  const [findPasswordModalOn, setFindPasswordModalOn] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false); // 로그인 상태 관리
  

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      setIsLoggedIn(true);
      axiosInstance.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${accessToken}`;
    } else {
      setIsLoggedIn(false);
      delete axiosInstance.defaults.headers.common["Authorization"];
    }
  }, []);

  const logo = "/everpet_logo.svg";
  const logo_text = "/everpet_logo_text.svg";

  const handleShowFindId = () => {
    setSignInModalOn(false);
    setFindIdModalOn(true);
  };

  const handleShowFindPassword = () => {
    setSignInModalOn(false);
    setFindPasswordModalOn(true);
  };

  const handleShowSignInFromId = () => {
    setFindIdModalOn(false);
    setSignInModalOn(true);
  };

  const handleShowSignInFromPassword = () => {
    setFindPasswordModalOn(false);
    setSignInModalOn(true);
  };

  const handleShowFindPasswordFromId = () => {
    setFindIdModalOn(false);
    setFindPasswordModalOn(true);
  };

  const handleShowFindIdFromPassword = () => {
    setFindPasswordModalOn(false);
    setFindIdModalOn(true);
  };


  const handleLogout = async () => {
    try {
      const localhostUrl = import.meta.env.VITE_APP_LOCALHOST_URL;
      await axiosInstance.post(`${localhostUrl}/user/logout`);
      localStorage.removeItem("accessToken");
      delete axiosInstance.defaults.headers.common["Authorization"]; // 헤더 초기화
      setIsLoggedIn(false);
      window.location.href = "/";
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <SignUpModal
        show={signUpModalOn}
        onHide={() => setsignUpModalOn(false)}
      />
      <SignInModal
        show={signInModalOn}
        onHide={() => setSignInModalOn(false)}
        onShowFindId={handleShowFindId}
        onShowFindPassword={handleShowFindPassword}
        setIsLoggedIn={setIsLoggedIn} // 로그인 상태 설정 함수 전달
      />
      <FindIdModal
        show={findIdModalOn}
        onHide={() => setFindIdModalOn(false)}
        onShowSignIn={handleShowSignInFromId}
        onShowFindPassword={handleShowFindPasswordFromId}
      />
      <FindPasswordModal
        show={findPasswordModalOn}
        onHide={() => setFindPasswordModalOn(false)}
        onShowSignIn={handleShowSignInFromPassword}
        onShowFindId={handleShowFindIdFromPassword}
      />
      <Navbar>
        <Container>
          <Navbar.Brand href="/">
            <img
              src={logo}
              alt="Everpet logo"
              width="50"
              height="50"
              className="d-inline-block align-top"
            />
            <img
              src={logo_text}
              alt="Everpet logo"
              height="50"
              className="d-inline-block align-top"
            />
          </Navbar.Brand>
          <Navbar.Collapse className="justify-content-end">
            <Nav>
              {isLoggedIn ? (
                <Button
                  type="button"
                  className="btn btn-main mx-2"
                  onClick={handleLogout}
                >
                  로그아웃
                </Button>
              ) : (
                <>
                  <Button
                    type="button"
                    className="btn btn-main mx-2"
                    onClick={() => setsignUpModalOn(true)}
                  >
                    회원가입
                  </Button>
                  <Button
                    type="button"
                    className="btn btn-main"
                    onClick={() => setSignInModalOn(true)}
                  >
                    로그인
                  </Button>
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
}

export default NavBar;
