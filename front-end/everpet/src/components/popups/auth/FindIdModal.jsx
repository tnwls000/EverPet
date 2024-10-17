import React, { useState } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import { Modal, Button, Form, Container } from "react-bootstrap";
import "@/css/button/Button.css";

const FindIdModal = ({ show, onHide, onShowSignIn, onShowFindPassword }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleFindId = async () => {
    try {
      const localhostUrl = import.meta.env.VITE_APP_LOCALHOST_URL;
      const response = await axios.get(`${localhostUrl}/user/find-id`, {
        params: { name, email },
      });

      const { userId } = response.data;
      setSuccess(`Your ID is: ${userId}`);
      setError(""); // Clear any previous error message
    } catch (error) {
      setError("아이디 찾기 실패: 이름 또는 이메일을 확인해주세요.");
      setSuccess(""); // Clear any previous success message
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
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            아이디 찾기
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="formBasicName">
              <Form.Label>이름</Form.Label>
              <Form.Control
                type="text"
                placeholder="이름을 입력해주세요"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>이메일</Form.Label>
              <Form.Control
                type="email"
                placeholder="이메일을 입력해주세요"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Form.Group>
            {error && <p className="text-danger">{error}</p>}
            {success && <p className="text-success">{success}</p>}
            <div className="d-flex justify-content-end">
              <Button
                className="btn btn-main"
                variant="info"
                type="button"
                onClick={handleFindId}
              >
                아이디 찾기
              </Button>
            </div>
          </Form>
          <div className="d-flex justify-content-end mt-3">
            <Button className ="custom-link-button" variant="link" onClick={onShowSignIn}>
              로그인
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

FindIdModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
  onShowSignIn: PropTypes.func.isRequired,
  onShowFindPassword: PropTypes.func.isRequired,
};

export default FindIdModal;
