import React, { useState, useEffect } from "react";
import axiosInstance from "@/api/AxiosInstance.js";
import { Button, Form, Container } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const RobotEdit = () => {
  const [robotData, setRobotData] = useState({
    robotSerialNumber: "",
    robotName: "",
    robotStyle: "",
    robotGender: "",
  });

  const [styles] = useState(["친근", "활발", "도도", "소심"]);
  const [genders] = useState(["수컷", "암컷"]);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchRobotData = async () => {
      try {
        const response = await axiosInstance.get("/robot");
        setRobotData({
          robotSerialNumber: response.data.robotSerialNumber,
          robotName: response.data.robotName,
          robotStyle: response.data.robotStyle,
          robotGender: response.data.robotGender,
        });
      } catch (error) {
        console.error("Failed to fetch robot data:", error);
      }
    };

    fetchRobotData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setRobotData({ ...robotData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form submitted with data:", robotData); // 디버깅 로그 추가

    try {
      const response = await axiosInstance.patch("/robot", {
        robotName: robotData.robotName,
        robotStyle: robotData.robotStyle,
        robotGender: robotData.robotGender,
      });
      console.log("Server response:", response); // 디버깅 로그 추가
      if (response.status === 200) {
        alert("로봇 정보가 수정되었습니다.");
        navigate("/mypage/robot-info");
      } else {
        alert(`Unexpected response status: ${response.status}`); // 예기치 않은 상태 코드 처리
      }
    } catch (error) {
      console.error("로봇 정보 수정 실패:", error);
      alert("로봇 정보 수정에 실패했습니다. 다시 시도해주세요.");
    }
  };

  return (
    <Container>
      <h2>로봇 정보 수정</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formRobotSerialNumber">
          <Form.Label>시리얼 번호</Form.Label>
          <Form.Control
            type="text"
            name="robotSerialNumber"
            value={robotData.robotSerialNumber}
            onChange={handleInputChange}
            disabled
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formRobotName">
          <Form.Label>이름</Form.Label>
          <Form.Control
            type="text"
            name="robotName"
            value={robotData.robotName}
            onChange={handleInputChange}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formRobotStyle">
          <Form.Label>스타일</Form.Label>
          <Form.Control
            as="select"
            name="robotStyle"
            value={robotData.robotStyle}
            onChange={handleInputChange}
            required
          >
            {styles.map((style, index) => (
              <option key={index} value={style}>
                {style}
              </option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formRobotGender">
          <Form.Label>성별</Form.Label>
          <Form.Control
            as="select"
            name="robotGender"
            value={robotData.robotGender}
            onChange={handleInputChange}
            required
          >
            {genders.map((gender, index) => (
              <option key={index} value={gender}>
                {gender}
              </option>
            ))}
          </Form.Control>
        </Form.Group>
        <Button variant="primary" type="submit" className="btn-main mx-2">
          수정 완료
        </Button>
        <Button
          variant="secondary"
          onClick={() => navigate("/mypage/robot-info")}
          className="btn-pink"
        >
          취소
        </Button>
      </Form>
    </Container>
  );
};

export default RobotEdit;
