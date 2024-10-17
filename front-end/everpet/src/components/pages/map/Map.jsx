import React, { useEffect, useRef, useState } from "react";
import { Button, Spinner, Container, Row, Col, Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import axiosInstance from "@/api/AxiosInstance";
import "@/css/button/Button.css";
import "@/css/Map.css";

const SLAMMap = ({ setLoading }) => {
  const [mapData, setMapData] = useState(null);
  const [serialNumber, setSerialNumber] = useState(null);
  const [isMapping, setIsMapping] = useState(false);

  const canvasRef = useRef(null);
  const pollingTimerRef = useRef(null);
  const url = import.meta.env.VITE_APP_LOCALHOST_URL;

  useEffect(() => {
    fetchMapData();

    const handleBeforeUnload = (event) => {
      if (isMapping) {
        event.preventDefault();
        event.returnValue = "";
      }
    };

    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
      if (pollingTimerRef.current) {
        clearInterval(pollingTimerRef.current);
        pollingTimerRef.current = null;
      }
    };
  }, [isMapping]);

  useEffect(() => {
    if (mapData) {
      drawMap(mapData);
    }
  }, [mapData]);

  const fetchMapData = async () => {
    try {
      const response = await axiosInstance.get(`${url}/map`);
      console.log(response.data);
      if (typeof response.data === "string") {
        setSerialNumber(response.data);
      } else {
        setSerialNumber(response.data.serialNumber);
        setMapData(response.data);
      }
    } catch (error) {
      console.error("지도 데이터를 가져오는 중 오류 발생:", error);
    }
  };

  const requestMapCreation = async () => {
    try {
      setLoading(true);
      setIsMapping(true);

      await axiosInstance.post(`${url}/mqtt/publish`, {
        topic: `${serialNumber}/jetson/map`,
        message: "requestMap",
      });

      console.log("requestMap 요청 전송");

      pollingTimerRef.current = setInterval(async () => {
        try {
          const response = await axiosInstance.get(`${url}/map`);
          console.log("지도 get 요청");
          if (typeof response.data !== "string") {
            setMapData(response.data);
          }
        } catch (error) {
          console.error("지도 데이터 확인 중 오류 발생:", error);
        }
      }, 3000);
    } catch (error) {
      console.error("지도 작성 요청 중 오류 발생:", error);
      setLoading(false);
    }
  };

  const stopMapCreation = async () => {
    try {
      await axiosInstance.post(`${url}/mqtt/publish`, {
        topic: `${serialNumber}/jetson/mapDone`,
        message: "mappingDone",
      });

      console.log("mappingDone 요청 전송");

      if (pollingTimerRef.current) {
        clearInterval(pollingTimerRef.current);
        pollingTimerRef.current = null;
      }

      setLoading(false);
      setIsMapping(false);
    } catch (error) {
      console.error("지도 종료 요청 중 오류 발생:", error);
      setLoading(false);
    }
  };

  const handleTabClick = (event) => {
    if (isMapping) {
      event.preventDefault(); // 탭 클릭 이벤트를 막음
      alert("지도 작성 중에는 다른 탭으로 이동할 수 없습니다.");
    }
  };

  const drawMap = (mapData) => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");

    const { width, height, resolution, data, positionX, positionY } = mapData;

    canvas.width = width;
    canvas.height = height;

    const imageData = context.createImageData(width, height);

    for (let i = 0; i < data.length; i++) {
      const value = data[i];
      const index = i * 4;

      let grayscale;
      if (value === 100) {
        grayscale = 0; // 검정색
      } else if (value === 0 || value === -1) {
        grayscale = 255; // 흰색
      } else {
        grayscale = 127; // 중간 회색, 필요하면 다른 값으로 수정 가능
      }

      imageData.data[index] = grayscale; // R
      imageData.data[index + 1] = grayscale; // G
      imageData.data[index + 2] = grayscale; // B
      imageData.data[index + 3] = 255; // A (불투명)
    }

    context.putImageData(imageData, 0, 0);

    const robotX = (positionX - positionX) / resolution;
    const robotY = height - (positionY - positionY) / resolution;

    context.fillStyle = "skyblue";
    context.beginPath();
    context.arc(robotX, robotY, 5, 0, 2 * Math.PI);
    context.fill();
  };

  return (
    <Container>
      <Row className="my-4">
        <Col>
          {isMapping && (
            <Alert variant="info">
              <Spinner animation="border" size="sm" /> 지도 작성 중입니다...
            </Alert>
          )}
          {mapData ? (
            <div>
              <canvas ref={canvasRef} className="border canvas" />
            </div>
          ) : serialNumber && !isMapping ? (
            <div>
              <Alert variant="warning">
                지도 데이터가 없습니다. 지도를 작성하려면 아래 버튼을
                클릭하세요.
              </Alert>
            </div>
          ) : serialNumber && !isMapping ? (
            <Alert variant="info">지도 데이터를 불러오는 중입니다...</Alert>
          ) : (
            <div></div>
          )}
          {isMapping ? (
            <Button
              variant="danger"
              onClick={stopMapCreation}
              className="btn btn-pink map-button"
            >
              지도 작성 종료
            </Button>
          ) : mapData ? (
            <Button
              variant="warning"
              onClick={requestMapCreation}
              className="btn btn-main map-button"
            >
              지도 재작성
            </Button>
          ) : (
            <Button
              variant="primary"
              onClick={requestMapCreation}
              className="btn btn-main map-button"
            >
              지도 작성
            </Button>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default SLAMMap;
