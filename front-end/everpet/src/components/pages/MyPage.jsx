import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Tabs, Tab, Container } from "react-bootstrap";
import AccessLog from "./mypage/AccessLog";
import UserInfo from "./mypage/UserInfo";
import RobotInfo from "./mypage/RobotInfo";
import SLAMMap from "./map/Map";
import DiaryList from "./diary/DiaryList";
import "@/css/Mypage.css";
import MyPageIcon from "./mypage/icon/MyPageIcon";
import DiaryIcon from "./mypage/icon/DiaryIcon";
import AccessLogIcon from "./mypage/icon/AccessLogIcon";
import RobotIcon from "./mypage/icon/RobotIcon";
import MapIcon from "./mypage/icon/MapIcon";

function MyPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeKey, setActiveKey] = useState("user-info");
  const [loading, setLoading] = useState(false); // loading 상태를 MyPage에서 관리

  useEffect(() => {
    const pathKey = location.pathname.split("/").pop();
    if (
      ["user-info", "robot-info", "access-log", "map", "diary"].includes(
        pathKey
      )
    ) {
      setActiveKey(pathKey);
    } else {
      setActiveKey("user-info"); // 기본값 설정
    }
  }, [location.pathname]);

  const handleSelect = (key) => {
    if (!loading) {
      // loading 중이 아닐 때만 탭 이동 허용
      navigate(`/mypage/${key}`);
    } else {
      alert("지도 작성 중에는 다른 탭으로 이동할 수 없습니다.");
    }
  };

  return (
    <Container>
      <Tabs activeKey={activeKey} onSelect={handleSelect} id="mypage-tabs">
        <Tab eventKey="user-info" title={<MyPageIcon />}>
          <div className="rounded-bottom-div">
            <UserInfo />
          </div>
        </Tab>
        <Tab eventKey="robot-info" title={<RobotIcon />}>
          <div className="rounded-bottom-div">
            <RobotInfo />
          </div>
        </Tab>
        <Tab eventKey="access-log" title={<AccessLogIcon />}>
          <div className="rounded-bottom-div">
            <AccessLog />
          </div>
        </Tab>
        <Tab eventKey="map" title={<MapIcon />}>
          <div className="rounded-bottom-div">
            <SLAMMap setLoading={setLoading} />{" "}
            {/* SLAMMap에 setLoading 전달 */}
          </div>
        </Tab>
        <Tab eventKey="diary" title={<DiaryIcon />}>
          <div className="rounded-bottom-div">
            <DiaryList />
          </div>
        </Tab>
      </Tabs>
    </Container>
  );
}

export default MyPage;
