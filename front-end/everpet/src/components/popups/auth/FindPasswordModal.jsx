// import PropTypes from 'prop-types';
// import { Modal, Button, Form, Container } from 'react-bootstrap';

// const FindPasswordModal = ({ show, onHide, onShowSignIn, onShowFindId }) => {
//   return (
//     <Container>
//       <Modal
//         show={show}
//         onHide={onHide}
//         size="lg"
//         aria-labelledby="contained-modal-title-vcenter"
//         centered
//       >
//         <Modal.Header closeButton>
//           <Modal.Title id="contained-modal-title-vcenter">
//             비밀번호 찾기
//           </Modal.Title>
//         </Modal.Header>
//         <Modal.Body>
//           <Form>
//             <Form.Group className="mb-3" controlId="formBasicID">
//               <Form.Label>아이디</Form.Label>
//               <Form.Control type="text" placeholder="아이디를 입력해주세요" />
//             </Form.Group>
//             <Form.Group className="mb-3" controlId="formBasicEmail">
//               <Form.Label>이메일</Form.Label>
//               <Form.Control type="email" placeholder="이메일을 입력해주세요" />
//             </Form.Group>
//             <div className="d-flex justify-content-end">
//               <Button className="btn btn-main" variant='info' type='button'>
//                 비밀번호 찾기
//               </Button>
//             </div>
//           </Form>
//           <div className="d-flex justify-content-end mt-3">
//             <Button className ="custom-link-button" variant="link" onClick={onShowSignIn}>로그인</Button>
//             <Button className ="custom-link-button" variant="link" >
//               |
//             </Button>
//             <Button className ="custom-link-button" variant="link" onClick={onShowFindId}>아이디 찾기</Button>
//           </div>
//         </Modal.Body>
//       </Modal>
//     </Container>
//   );
// };

// FindPasswordModal.propTypes = {
//   show: PropTypes.bool.isRequired,
//   onHide: PropTypes.func.isRequired,
//   onShowSignIn: PropTypes.func.isRequired,
//   onShowFindId: PropTypes.func.isRequired,
// };

// export default FindPasswordModal;

import PropTypes from 'prop-types';
import { useState } from 'react';
import { Modal, Button, Form, Container, Alert } from 'react-bootstrap';
import axios from 'axios';

const localhostUrl = import.meta.env.VITE_APP_LOCALHOST_URL;

const FindPasswordModal = ({ show, onHide, onShowSignIn, onShowFindId }) => {
  const [userId, setUserId] = useState('');
  const [email, setEmail] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleFindPassword = async () => {
    try {
      const response = await axios.post(`${localhostUrl}/user/find-password`, {
        userId,
        email,
      });

      if (response.status === 200) {
        setSuccessMessage('임시 비밀번호가 이메일로 전송되었습니다.');
        setErrorMessage('');
      } else if (response.status === 404) {
        setErrorMessage('일치하는 아이디와 이메일이 없습니다.');
        setSuccessMessage('');
      } else {
        setErrorMessage('비밀번호 찾기에 실패했습니다. 다시 시도해주세요.');
        setSuccessMessage('');
      }
    } catch (error) {
      console.error("비밀번호 찾기 오류:", error);
      setErrorMessage('서버와 통신하는 동안 오류가 발생했습니다.');
      setSuccessMessage('');
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
            비밀번호 찾기
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="formBasicID">
              <Form.Label>아이디</Form.Label>
              <Form.Control
                type="text"
                placeholder="아이디를 입력해주세요"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
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
            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
            {successMessage && <Alert variant="success">{successMessage}</Alert>}
            <div className="d-flex justify-content-end">
              <Button
                className="btn btn-main"
                variant="info"
                type="button"
                onClick={handleFindPassword}
              >
                비밀번호 찾기
              </Button>
            </div>
          </Form>
          <div className="d-flex justify-content-end mt-3">
            <Button className="custom-link-button" variant="link" onClick={onShowSignIn}>
              로그인
            </Button>
            <Button className="custom-link-button" variant="link">
              |
            </Button>
            <Button className="custom-link-button" variant="link" onClick={onShowFindId}>
              아이디 찾기
            </Button>
          </div>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

FindPasswordModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
  onShowSignIn: PropTypes.func.isRequired,
  onShowFindId: PropTypes.func.isRequired,
};

export default FindPasswordModal;