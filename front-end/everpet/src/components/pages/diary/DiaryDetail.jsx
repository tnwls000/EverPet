import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axiosInstance from "@/api/AxiosInstance";
import { Button, Modal, Form } from "react-bootstrap";
import "@/css/button/Button.css";
import "@/css/DiaryDetail.css";
import GearIcon from "../mypage/icon/GearIcon";
import BackIcon from "../mypage/icon/BackIcon";

const url = import.meta.env.VITE_APP_LOCALHOST_URL;

const DiaryDetail = () => {
  const { id } = useParams();
  const [diary, setDiary] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [diaryContent, setDiaryContent] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showActions, setShowActions] = useState(false);
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate("/mypage/diary");
  };

  useEffect(() => {
    const fetchDiary = async () => {
      const response = await axiosInstance.get(`${url}/diary/${id}`);
      setDiary(response.data);
      setDiaryContent(response.data.diaryContent);
    };
    fetchDiary();
  }, [id]);

  const handleSave = async () => {
    await axiosInstance.patch(`${url}/diary/${id}`, {
      diaryId: id,
      content: diaryContent,
    });
    setDiary((prevDiary) => ({
      ...prevDiary,
      diaryContent: diaryContent,
    }));
    setIsEditing(false);
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleDelete = async () => {
    await axiosInstance.delete(`${url}/diary/${id}`);
    navigate("/mypage/diary");
  };

  const renderDiaryContent = () => {
    return diaryContent
      .split(/(?<=[."'])\s+/)
      .filter(Boolean)
      .map((paragraph, index) => <p key={index}>{paragraph}</p>);
  };

  const calculateRows = (text) => {
    return text.split(/(?<=[.!?"'])\s+/).length;
  };

  if (!diary) return <div>Loading...</div>;

  return (
    <div className="diary-detail-container">
      <div className="diary-detail-btns">
        <Button className="diary-back-button detail-btn" onClick={handleGoBack}>
          <BackIcon />
        </Button>

        {!isEditing && (
          <div className="edit-delete-btns">
            <Button
              className="btn btn-main mx-2 detail-btn"
              onClick={handleEdit}
            >
              수정
            </Button>
            <Button
              className="btn btn-pink detail-btn"
              onClick={() => setShowDeleteModal(true)}
            >
              삭제
            </Button>
          </div>
        )}
      </div>

      <div className="diary-content-wrapper">
        {diary.imageUrl && (
          <img
            src={diary.imageUrl}
            alt={diary.diaryContent}
            className="diary-image"
          />
        )}

        <div className="edit-div">
          <div className="diary-detail-date">{diary.createTime}</div>
          {isEditing ? (
            <div className="edit-container">
              <div className="diary-text">
                <Form.Control
                  as="textarea"
                  rows={calculateRows(diaryContent)}
                  value={diaryContent}
                  onChange={(e) => setDiaryContent(e.target.value)}
                  className="edit-textarea"
                />
              </div>
              <div className="save-cancel-btns">
                <Button
                  className="btn btn-main mx-2 detail-btn"
                  onClick={handleSave}
                >
                  저장
                </Button>
                <Button
                  className="btn btn-pink detail-btn"
                  onClick={() => setIsEditing(false)}
                >
                  취소
                </Button>
              </div>
            </div>
          ) : (
            <div className="diary-text">
              <p>{renderDiaryContent()}</p>
            </div>
          )}
        </div>
      </div>
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>다이어리 삭제</Modal.Title>
        </Modal.Header>
        <Modal.Body>정말 삭제하시겠습니까?</Modal.Body>
        <Modal.Footer>
          <Button
            className="btn btn-main detail-btn"
            onClick={() => setShowDeleteModal(false)}
          >
            취소
          </Button>
          <Button className="btn btn-pink detail-btn" onClick={handleDelete}>
            삭제
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default DiaryDetail;
