import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "@/api/AxiosInstance.js";
import { Container, Alert, Table, Button } from "react-bootstrap";
import "@/css/button/Button.css";
import "@/css/Table.css";

const RobotInfo = () => {
  const [robotData, setRobotData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRobotData = async () => {
      try {
        const response = await axiosInstance.get("/robot");
        setRobotData(response.data);
      } catch (error) {
        setError("로봇 정보를 불러오는데 실패했습니다.");
      }
    };

    fetchRobotData();
  }, []);

  const handleEditClick = () => {
    navigate("/robot/edit");
  };

  return (
    <Container>
      <h2>로봇 정보 조회</h2>
      {error && <Alert variant="danger">{error}</Alert>}
      {robotData ? (
        <>
          <Table bordered hover className="custom-table">
            <tbody>
              <tr>
                <th>로봇 시리얼 번호</th>
                <td>{robotData.robotSerialNumber}</td>
              </tr>
              <tr>
                <th>로봇 이름</th>
                <td>{robotData.robotName}</td>
              </tr>
              <tr>
                <th>로봇 스타일</th>
                <td>{robotData.robotStyle}</td>
              </tr>
              <tr>
                <th>로봇 성별</th>
                <td>{robotData.robotGender}</td>
              </tr>
            </tbody>
          </Table>
          <div className="d-flex justify-content-md-end">
            <Button
              className="btn-main"
              variant="primary"
              onClick={handleEditClick}
            >
              수정
            </Button>
          </div>
        </>
      ) : (
        !error && <p>로봇 정보를 불러오는 중입니다...</p>
      )}
    </Container>
  );
};

export default RobotInfo;
