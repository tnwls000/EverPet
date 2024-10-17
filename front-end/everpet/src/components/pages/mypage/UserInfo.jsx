import React, { useState, useEffect } from "react";
import axiosInstance from "@/api/AxiosInstance.js";
import { Container, Table, Alert, Button, Modal, Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import "@/css/button/Button.css";
import "@/css/Table.css";

const localhostUrl = import.meta.env.VITE_APP_LOCALHOST_URL; // localhostUrl 정의

const UserInfo = () => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false); // 모달 표시 상태
  const [password, setPassword] = useState(""); // 입력된 비밀번호
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axiosInstance.get(`${localhostUrl}/user`);
        setUserData(response.data);
      } catch (error) {
        setError("회원 정보를 불러오는데 실패했습니다.");
      }
    };

    fetchUserData();
  }, []);

  const handleEdit = () => {
    navigate("/user/edit");
  };

  const handleDelete = async () => {
    try {
      const response = await axiosInstance.delete(`${localhostUrl}/user`, {
        params: { password }, // 비밀번호를 서버로 전송
      });
      if (response.status === 204) {
        localStorage.removeItem("accessToken");
        delete axiosInstance.defaults.headers.common["Authorization"];
        alert("회원 탈퇴가 완료되었습니다.");
        navigate("/");
        window.location.reload();
      }
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setError("비밀번호가 일치하지 않습니다.");
      } else {
        setError("회원 탈퇴에 실패했습니다.");
      }
    }
  };

  const openModal = () => {
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setPassword(""); // 비밀번호 초기화
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleConfirmDelete = () => {
    closeModal();
    handleDelete();
  };

  return (
    <Container>
      <h2>회원 정보</h2>
      {error && <Alert variant="danger">{error}</Alert>}
      {userData ? (
        <>
          <Table className="custom-table" bordered hover>
            <tbody>
              <tr>
                <th>아이디</th>
                <td>{userData.userId}</td>
              </tr>
              <tr>
                <th>이름</th>
                <td>{userData.name}</td>
              </tr>
              <tr>
                <th>이메일</th>
                <td>{userData.email}</td>
              </tr>
              <tr>
                <th>전화번호</th>
                <td>{userData.phoneNumber}</td>
              </tr>
              <tr>
                <th>성별</th>
                <td>{userData.gender}</td>
              </tr>
              <tr>
                <th>나이</th>
                <td>{userData.age}</td>
              </tr>
            </tbody>
          </Table>
          <div className="d-flex justify-content-md-end">
            <Button
              className="btn-main mx-2"
              variant="primary"
              onClick={handleEdit}
            >
              수정
            </Button>
            <Button
              variant="danger"
              onClick={openModal} // 모달 열기
              className="btn-pink"
            >
              탈퇴
            </Button>
          </div>
        </>
      ) : (
        <p>로딩 중...</p>
      )}

      {/* 회원 탈퇴 비밀번호 입력 모달 */}
      <Modal show={showModal} onHide={closeModal}>
        <Modal.Header closeButton>
          <Modal.Title>회원 탈퇴</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group controlId="formPassword">
            <Form.Label>비밀번호를 입력하세요</Form.Label>
            <Form.Control
              type="password"
              placeholder="비밀번호"
              value={password}
              onChange={handlePasswordChange}
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={closeModal}
            className="btn btn-main"
          >
            취소
          </Button>
          <Button
            variant="danger"
            onClick={handleConfirmDelete}
            className="btn btn-pink"
          >
            탈퇴
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default UserInfo;
