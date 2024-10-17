import React, { useState, useEffect } from "react";
import axiosInstance from "@/api/AxiosInstance.js";
import { Button, Form, InputGroup, Container } from "react-bootstrap";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const UserEdit = () => {
  const [formData, setFormData] = useState({
    name: "",
    password: "",
    newPassword: "",
    confirmNewPassword: "",
    email: "",
    phoneNumber: "",
    gender: "",
    age: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmNewPassword, setShowConfirmNewPassword] = useState(false);
  const [passwordsMatch, setPasswordsMatch] = useState(true);
  const [isEmailValid, setIsEmailValid] = useState(true);
  const [isPhoneValid, setIsPhoneValid] = useState(true);
  const [isAgeValid, setIsAgeValid] = useState(true);
  const [emailSent, setEmailSent] = useState(false);
  const [inputVerificationCode, setInputVerificationCode] = useState("");
  const [isVerified, setIsVerified] = useState(false);
  const [timer, setTimer] = useState(180); // 3분 (180초) 타이머
  const navigate = useNavigate();

  useEffect(() => {
    if (emailSent && timer > 0 && !isVerified) {
      const countdown = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);

      return () => clearInterval(countdown);
    } else if (timer === 0) {
      setEmailSent(false);
      setTimer(180); // 타이머 초기화
    }
  }, [emailSent, timer, isVerified]);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axiosInstance.get("/user");
        setFormData({
          name: response.data.name,
          email: response.data.email,
          phoneNumber: response.data.phoneNumber,
          gender: response.data.gender,
          age: response.data.age,
          password: "",
          newPassword: "",
          confirmNewPassword: "",
        });
        setIsVerified(true); // 이메일 인증 상태를 기본으로 true로 설정 (이미 인증된 사용자)
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      }
    };
    fetchUserData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    if (name === "email") {
      const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
      setIsEmailValid(emailValid);
    }

    if (name === "phoneNumber") {
      const phoneValid = /^[0-9]{10,11}$/.test(value);
      setIsPhoneValid(phoneValid);
    }

    if (name === "age") {
      const ageValid = /^[0-9]{1,3}$/.test(value) && value >= 0 && value <= 120;
      setIsAgeValid(ageValid);
    }

    if (name === "newPassword" || name === "confirmNewPassword") {
      setPasswordsMatch(formData.newPassword === value);
    }
  };

  const sendVerificationEmail = async () => {
    try {
      const response = await axiosInstance.post("/email/verification", null, {
        params: { email: formData.email },
      });
      if (response.status === 200) {
        setEmailSent(true);
        setTimer(180); // 타이머 3분으로 초기화
        setInputVerificationCode(""); // 이전 인증 코드 무효화
        setIsVerified(false); // 이전 인증 상태 초기화
        alert("인증 코드가 이메일로 전송되었습니다.");
      }
    } catch (error) {
      if (error.response && error.response.status === 409) {
        // 이메일 중복 에러 처리
        alert("이미 존재하는 이메일입니다. 다른 이메일을 사용해주세요.");
      } else {
        console.error("이메일 전송 오류:", error);
        alert("인증 코드 전송에 실패했습니다. 다시 시도해주세요.");
      }
    }
  };

  const handleVerifyCode = async () => {
    try {
      const response = await axiosInstance.get("/email/verification", {
        params: { verificationCode: inputVerificationCode },
      });
      if (response.status === 200) {
        setIsVerified(true);
        alert("이메일 인증에 성공했습니다.");
      } else {
        alert("인증 코드가 일치하지 않습니다. 다시 시도해주세요.");
      }
    } catch (error) {
      console.error("코드 인증 오류:", error);
      alert("인증 코드 확인에 실패했습니다. 다시 시도해주세요.");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!passwordsMatch) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      const response = await axiosInstance.patch("/user", {
        ...formData,
        newPassword: formData.newPassword || null, // 새 비밀번호가 없을 경우 null로 전송
      });
      if (response.status === 201) {
        alert("회원 정보 수정이 완료되었습니다.");
        navigate("/mypage/user-info");
      }
    } catch (error) {
      if (error.response && error.response.status === 409) {
        alert("현재 비밀번호가 일치하지 않습니다. 다시 시도해주세요.");
      } else {
        console.error("회원 정보 수정 실패:", error);
        alert("회원 정보 수정에 실패했습니다. 다시 시도해주세요.");
      }
    }
  };

  const toggleShowPassword = () => setShowPassword(!showPassword);
  const toggleShowNewPassword = () => setShowNewPassword(!showNewPassword);
  const toggleShowConfirmNewPassword = () =>
    setShowConfirmNewPassword(!showConfirmNewPassword);

  return (
    <Container>
      <h2>회원 정보 수정</h2>
      <Form>
        <Form.Group className="mb-3" controlId="formBasicName">
          <Form.Label>이름</Form.Label>
          <Form.Control
            type="text"
            placeholder="이름을 입력해주세요"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>현재 비밀번호</Form.Label>
          <InputGroup>
            <Form.Control
              type={showPassword ? "text" : "password"}
              placeholder="현재 비밀번호를 입력해주세요"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
            />
            <Button variant="outline-secondary" onClick={toggleShowPassword}>
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </Button>
          </InputGroup>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicNewPassword">
          <Form.Label>새 비밀번호</Form.Label>
          <InputGroup>
            <Form.Control
              type={showNewPassword ? "text" : "password"}
              placeholder="새 비밀번호를 입력해주세요"
              name="newPassword"
              value={formData.newPassword}
              onChange={handleInputChange}
            />
            <Button
              variant="outline-secondary"
              onClick={() => setShowNewPassword(!showNewPassword)}
            >
              {showNewPassword ? <FaEyeSlash /> : <FaEye />}
            </Button>
          </InputGroup>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicConfirmNewPassword">
          <Form.Label>새 비밀번호 확인</Form.Label>
          <InputGroup>
            <Form.Control
              type={showConfirmNewPassword ? "text" : "password"}
              placeholder="새 비밀번호를 다시 입력해주세요"
              name="confirmNewPassword"
              value={formData.confirmNewPassword}
              onChange={handleInputChange}
            />
            <Button
              variant="outline-secondary"
              onClick={() => setShowConfirmNewPassword(!showConfirmNewPassword)}
            >
              {showConfirmNewPassword ? <FaEyeSlash /> : <FaEye />}
            </Button>
          </InputGroup>
          {!passwordsMatch && (
            <Form.Text className="text-danger">
              비밀번호가 일치하지 않습니다.
            </Form.Text>
          )}
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>이메일</Form.Label>
          <InputGroup>
            <Form.Control
              type="email"
              placeholder="이메일을 입력해주세요"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
            />
            <Button
              variant="outline-secondary"
              onClick={sendVerificationEmail}
              disabled={!isEmailValid}
            >
              {emailSent ? "인증 코드 재전송" : "인증 코드 보내기"}
            </Button>
          </InputGroup>
          {!isEmailValid && (
            <Form.Text className="text-danger">
              유효한 이메일 주소를 입력해주세요.
            </Form.Text>
          )}
          {!isVerified && (
            <div>
              {emailSent && timer > 0 && (
                <Form.Text className="text-info">
                  인증 코드 유효 시간: {Math.floor(timer / 60)}:
                  {timer % 60 < 10 ? `0${timer % 60}` : timer % 60}
                </Form.Text>
              )}
            </div>
          )}
        </Form.Group>
        {emailSent && (
          <Form.Group className="mb-3" controlId="formBasicVerificationCode">
            <Form.Label>인증 코드</Form.Label>
            <InputGroup>
              <Form.Control
                type="text"
                placeholder="이메일로 받은 인증 코드를 입력해주세요"
                value={inputVerificationCode}
                onChange={(e) => setInputVerificationCode(e.target.value)}
              />
              <Button
                variant="outline-secondary"
                onClick={handleVerifyCode}
                disabled={!inputVerificationCode}
              >
                인증
              </Button>
            </InputGroup>
          </Form.Group>
        )}
        <Form.Group className="mb-3" controlId="formBasicPhoneNumber">
          <Form.Label>전화번호</Form.Label>
          <Form.Control
            type="text"
            placeholder="전화번호를 입력해주세요"
            name="phoneNumber"
            value={formData.phoneNumber}
            onChange={handleInputChange}
          />
          {!isPhoneValid && (
            <Form.Text className="text-danger">
              유효한 전화번호를 입력해주세요.
            </Form.Text>
          )}
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicGender">
          <Form.Label>성별</Form.Label>
          <Form.Control
            as="select"
            name="gender"
            value={formData.gender}
            onChange={handleInputChange}
          >
            <option value="">선택하세요</option>
            <option value="male">남성</option>
            <option value="female">여성</option>
            <option value="other">기타</option>
          </Form.Control>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicAge">
          <Form.Label>나이</Form.Label>
          <Form.Control
            type="number"
            placeholder="나이를 입력해주세요"
            name="age"
            value={formData.age}
            onChange={handleInputChange}
          />
          {!isAgeValid && (
            <Form.Text className="text-danger">
              유효한 나이를 입력해주세요.
            </Form.Text>
          )}
        </Form.Group>
      </Form>
      <Button
        variant="primary"
        onClick={handleSubmit}
        disabled={!isVerified || !passwordsMatch}
        className="btn-main mx-2"
      >
        수정 완료
      </Button>
      <Button
        variant="secondary"
        onClick={() => navigate("/mypage")}
        className="btn-pink"
      >
        취소
      </Button>
    </Container>
  );
};

export default UserEdit;
