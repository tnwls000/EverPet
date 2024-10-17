import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "react-bootstrap";
import axiosInstance from "@/api/AxiosInstance";
import DiaryCreateModal from "./DiaryCreateModal";
import "@/css/button/Button.css";
import "@/css/DiaryList.css";

const DiaryList = () => {
  const [diaries, setDiaries] = useState([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchDiaries = async () => {
      const url = import.meta.env.VITE_APP_LOCALHOST_URL;
      const response = await axiosInstance.get(`${url}/diary`);
      setDiaries(response.data);
    };
    fetchDiaries();
  }, []);

  const handleShowModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);

  const handleSaveDiary = async () => {
    const url = import.meta.env.VITE_APP_LOCALHOST_URL;
    const response = await axiosInstance.get(`${url}/diary`);
    setDiaries(response.data);
  };

  return (
    <div className="diary-list-container">
      <div className="button-container">
        <Button className="btn btn-main" onClick={handleShowModal}>
          다이어리 작성
        </Button>
      </div>
      <div className="diary-list">
        {diaries.length === 0 ? (
          <p>작성된 다이어리가 없습니다.</p>
        ) : (
          diaries.map((diary) => (
            <div key={diary.diaryId} className="diary-item">
              <Link to={`/diary/${diary.diaryId}`}>
                <img src={diary.imageUrl} alt={diary.title} />
              </Link>
              <div className="diary-date">{diary.createTime}</div>
            </div>
          ))
        )}
      </div>

      <DiaryCreateModal
        show={showModal}
        handleClose={handleCloseModal}
        onSave={handleSaveDiary}
      />
    </div>
  );
};

export default DiaryList;
