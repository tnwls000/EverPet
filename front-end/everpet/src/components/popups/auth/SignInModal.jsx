// import React,
import { useState } from "react";
import PropTypes from "prop-types";
import axiosInstance from "@/api/AxiosInstance.js";
// import axios from "axios";
import { Modal, Button, Form, Container } from "react-bootstrap";
import "@/css/button/Button.css";

const SignInModal = ({
  show,
  onHide,
  onShowFindId,
  onShowFindPassword,
  setIsLoggedIn,
}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    // Prevent the default form submission behavior
    if (e) e.preventDefault();

    try {
      console.log(
        "Environment Variable:",
        import.meta.env.VITE_APP_LOCALHOST_URL
      );
      const localhostUrl = import.meta.env.VITE_APP_LOCALHOST_URL;
      const response = await axiosInstance.post(`${localhostUrl}/user/login`, {
        userId: username,
        password: password,
      });

      const accessToken = response.headers["accesstoken"];
      localStorage.setItem("accessToken", accessToken);

      setIsLoggedIn(true);
      onHide();
      window.location.href = "/mypage";
    } catch (error) {
      setError("로그인 실패: 아이디 또는 비밀번호를 확인해주세요.");
    }
  };

  return (
    <Container>
      <Modal
        show={show}
        onHide={onHide}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        backdrop="static"
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">로그인</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleLogin}>
            <Form.Group className="mb-3" controlId="formBasicID">
              <Form.Label>아이디</Form.Label>
              <Form.Control
                type="text"
                placeholder="아이디를 입력해주세요"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>비밀번호</Form.Label>
              <Form.Control
                type="password"
                placeholder="비밀번호를 입력해주세요"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>
            {error && <p className="text-danger">{error}</p>}
            <div className="d-flex justify-content-end">
              <Button
                className="btn btn-main"
                variant="info"
                type="submit" 
              >
                로그인
              </Button>
            </div>
          </Form>
          <div className="d-flex justify-content-end mt-3">
            <Button className ="custom-link-button" variant="link" onClick={onShowFindId}>
              아이디 찾기
            </Button>
            <Button className ="custom-link-button" variant="link" >
              |
            </Button>
            <Button className ="custom-link-button" variant="link" onClick={onShowFindPassword}>
              비밀번호 찾기
            </Button>
          </div>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

SignInModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
  onShowFindId: PropTypes.func.isRequired,
  onShowFindPassword: PropTypes.func.isRequired,
  setIsLoggedIn: PropTypes.func.isRequired,
};

export default SignInModal;