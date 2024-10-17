import React, { useState, useEffect } from "react";
import axiosInstance from "@/api/AxiosInstance.js";
import { Container, Form, Button, Table } from "react-bootstrap";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "@/css/button/Button.css";
import "@/css/Table.css";
import "@/css/AccessLog.css"; // 추가된 CSS 파일

const AccessLog = () => {
  const [accessLogs, setAccessLogs] = useState([]);
  const [accessType, setAccessType] = useState("");
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  useEffect(() => {
    fetchAccessLogs();
  }, []);

  const fetchAccessLogs = async () => {
    try {
      let params = {};

      if (accessType) {
        params.accessType = accessType;
      }

      if (startDate) {
        params.startDate = startDate.toISOString();
      }
      if (endDate) {
        params.endDate = endDate.toISOString();
      }

      const url = import.meta.env.VITE_APP_LOCALHOST_URL;
      const response = await axiosInstance.get(`${url}/access`, { params });
      setAccessLogs(response.data);
    } catch (error) {
      console.error("Failed to fetch access logs:", error);
    }
  };

  const handleSearch = () => {
    fetchAccessLogs();
  };

  return (
    <Container className="access-log-container">
      <h2>출입 기록</h2>
      <Form className="mb-5">
        <div className="row g-3">
          <div className="col-md-9 d-flex flex-wrap">
            <Form.Group
              controlId="accessType"
              className="d-flex align-items-center flex-grow-1 access-form-group"
            >
              <Form.Label className="access-form-label">유형</Form.Label>
              <Form.Control
                as="select"
                value={accessType}
                onChange={(e) => setAccessType(e.target.value)}
                className="custom-form-control"
              >
                <option value="">선택</option>
                <option value="IN">귀가</option>
                <option value="OUT">외출</option>
              </Form.Control>
            </Form.Group>

            <Form.Group
              controlId="startDate"
              className="d-flex align-items-center flex-grow-1 access-form-group"
            >
              <Form.Label className="access-form-label">시작일</Form.Label>
              <DatePicker
                selected={startDate}
                onChange={(date) => setStartDate(date)}
                showTimeSelect
                dateFormat="Pp"
                isClearable
                className="custom-datepicker"
              />
            </Form.Group>

            <Form.Group
              controlId="endDate"
              className="d-flex align-items-center flex-grow-1 access-form-group"
            >
              <Form.Label className="access-form-label">종료일</Form.Label>
              <DatePicker
                selected={endDate}
                onChange={(date) => setEndDate(date)}
                showTimeSelect
                dateFormat="Pp"
                isClearable
                className="custom-datepicker"
              />
            </Form.Group>
          </div>

          <div className="col-md-3 d-flex justify-content-md-end mt-3 mt-md-0 access-search-btn-container">
            <Button
              className="btn-main access-search-btn"
              onClick={handleSearch}
            >
              Search
            </Button>
          </div>
        </div>
      </Form>
      <Table bordered hover>
        <thead>
          <tr>
            <th>번호</th>
            <th>출입 시간</th>
            <th>출입 유형</th>
          </tr>
        </thead>
        <tbody>
          {accessLogs.map((log, index) => (
            <tr key={log.accessId}>
              <td>{index + 1}</td>
              <td>{new Date(log.accessTime).toLocaleString()}</td>
              <td>{log.accessType === "IN" ? "귀가" : "외출"}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default AccessLog;
