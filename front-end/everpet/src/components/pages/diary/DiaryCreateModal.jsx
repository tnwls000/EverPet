import React, { useState } from "react";
import { Modal, Button, Form, Spinner } from "react-bootstrap";
import axiosInstance from "@/api/AxiosInstance";
import "@/css/button/Button.css";

const DiaryCreateModal = ({ show, handleClose, onSave }) => {
  const [diaryContent, setDiaryContent] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  const isContentEmpty = diaryContent.trim() === "";

  const handleSaveDiary = async () => {
    const url = import.meta.env.VITE_APP_LOCALHOST_URL;

    setIsSaving(true);

    try {
      await axiosInstance.post(`${url}/diary`, { content: diaryContent });
      onSave();
      handleClose();
    } catch (error) {
      console.error("다이어리 작성에 실패했습니다.", error);
      alert("다이어리 작성에 실패했습니다.");
    } finally {
      setIsSaving(false); // 저장 완료
    }
  };

  return (
    <Modal
      show={show}
      onHide={() => (isSaving ? null : handleClose())}
      aria-labelledby="contained-modal-title-vcenter"
      centered
      backdrop={isSaving ? "static" : "true"}
    >
      <Modal.Header closeButton>
        <Modal.Title>다이어리 작성</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="formDiaryContent">
            <Form.Label>내용</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={diaryContent}
              onChange={(e) => setDiaryContent(e.target.value)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button
          className="btn btn-pink"
          onClick={handleClose}
          disabled={isSaving}
        >
          취소
        </Button>
        <Button
          className="btn btn-main"
          onClick={handleSaveDiary}
          disabled={isContentEmpty || isSaving}
        >
          {isSaving ? (
            <>
              <span className="ms-2">다이어리 작성 중... </span>
              <Spinner
                as="span"
                animation="border"
                size="sm"
                role="status"
                aria-hidden="true"
              />
            </>
          ) : (
            "작성하기"
          )}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default DiaryCreateModal;
