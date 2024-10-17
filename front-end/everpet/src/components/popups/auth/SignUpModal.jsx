import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import axios from "axios"; // axios 추가
import { Modal, Button, Form, Container, InputGroup } from "react-bootstrap";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import "@/css/button/Button.css";

const SignUpModal = ({ show, onHide }) => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    userId: "",
    password: "",
    confirmPassword: "",
    name: "",
    email: "",
    phoneNumber: "",
    robotSerialNumber: "",
    robotName: "",
    robotStyle: "",
    robotGender: "",
    gender: "",
    age: "",
  });
  const [isUsernameLocked, setIsUsernameLocked] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isUsernameValid, setIsUsernameValid] = useState(true);
  const [isUsernameAvailable, setIsUsernameAvailable] = useState(true);
  const [isPasswordValid, setIsPasswordValid] = useState(true);
  const [isEmailValid, setIsEmailValid] = useState(true);
  const [isPhoneValid, setIsPhoneValid] = useState(true);
  const [isSerialValid, setIsSerialValid] = useState(false);
  const [isRobotNameValid, setIsRobotNameValid] = useState(true); // 추가된 상태
  const [isAgeValid, setIsAgeValid] = useState(true);
  const [passwordsMatch, setPasswordsMatch] = useState(true);
  const [emailSent, setEmailSent] = useState(false);
  const [inputVerificationCode, setInputVerificationCode] = useState("");
  const [isVerified, setIsVerified] = useState(false);
  const [serialVerificationResult, setSerialVerificationResult] = useState("");
  const [usernameVerificationResult, setUsernameVerificationResult] =
    useState("");
  const [timer, setTimer] = useState(180); // 3분 (180초) 타이머
  const localhostUrl = import.meta.env.VITE_APP_LOCALHOST_URL;

  useEffect(() => {
    if (show) {
      setStep(1);
      setFormData({
        userId: "",
        password: "",
        confirmPassword: "",
        name: "",
        email: "",
        phoneNumber: "",
        robotSerialNumber: "",
        robotName: "",
        robotStyle: "",
        robotGender: "",
        gender: "",
        age: "",
      });
      setIsUsernameValid(true);
      setIsUsernameAvailable(true);
      setIsPasswordValid(true);
      setIsEmailValid(true);
      setIsPhoneValid(true);
      setIsSerialValid(false);
      setIsRobotNameValid(true); // 초기화 추가
      setPasswordsMatch(true);
      setEmailSent(false);
      setInputVerificationCode("");
      setIsVerified(false);
      setFormData({ userId: "" });
      setIsUsernameAvailable(false);
      setUsernameVerificationResult("");
      setIsUsernameLocked(false);
      setIsAgeValid(true);
    }
  }, [show]);

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

  // 아이디 확인 함수
  const handleCheckUsername = async () => {
    if (formData.userId.length < 3) {
      setIsUsernameAvailable(false);
      setUsernameVerificationResult("아이디는 3자 이상 입력해야 합니다.");
      return;
    }

    try {
      const response = await axios.get(`${localhostUrl}/user/validate-id`, {
        params: { userId: formData.userId },
      });

      if (response.status === 200) {
        setIsUsernameAvailable(true);
        setUsernameVerificationResult("사용 가능한 아이디입니다.");
        setIsUsernameLocked(true); // 아이디 입력 필드 고정
      }
    } catch (error) {
      setIsUsernameAvailable(false);
      if (error.response && error.response.status === 409) {
        setUsernameVerificationResult("중복된 아이디입니다.");
      } else {
        setUsernameVerificationResult("오류가 발생했습니다.");
      }
    }
  };

  const handleResetUsername = () => {
    setFormData({ ...formData, userId: "" });
    setIsUsernameAvailable(false);
    setUsernameVerificationResult("");
    setIsUsernameLocked(false);
  };

  const handleInputChange = async (e) => {
    const { name, value } = e.target;
    const updatedFormData = {
      ...formData,
      [name]: value,
    };
    setFormData(updatedFormData);

    // 유효성 검사
    if (name === "userId") {
      const regex = /^[a-zA-Z0-9]*$/;
      if (!regex.test(value)) {
        setIsUsernameValid(false);
        setUsernameVerificationResult(
          "아이디는 영어와 숫자만 입력할 수 있습니다."
        );
        return;
      }

      setIsUsernameValid(true);
      setUsernameVerificationResult(""); // 유효성 검사 초기화

      if (value.length < 3) {
        setIsUsernameValid(false);
        setUsernameVerificationResult("아이디는 3글자 이상이어야 합니다.");
        setIsUsernameAvailable(false);
        return;
      }

      setIsUsernameValid(value.length >= 3);
      setIsUsernameAvailable(true); // 기본적으로 입력 중에는 사용 가능한 상태로 설정
      setUsernameVerificationResult(""); // 검증 결과 초기화
      if (value.length >= 3) {
        try {
          const response = await axios.get(`${localhostUrl}/user/validate-id`, {
            params: { userId: value },
          });
          setIsUsernameAvailable(response.status === 200);
        } catch (error) {
          setIsUsernameAvailable(false);
        }
      } else {
        setIsUsernameAvailable(false);
      }
    }
    if (name === "password") {
      const passwordValid =
        /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(
          value
        );
      setIsPasswordValid(passwordValid);
    }
    if (name === "confirmPassword") {
      setPasswordsMatch(value === formData.password);
    }
    if (name === "email") {
      const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
      setIsEmailValid(emailValid);
    }
    if (name === "phoneNumber") {
      const phoneValid = /^[0-9]{10,11}$/.test(value);
      setIsPhoneValid(phoneValid);
    }
    if (name === "robotSerialNumber") {
      setIsSerialValid(false); // 입력 중에는 기본적으로 유효하지 않다고 설정
      setSerialVerificationResult(""); // 검증 결과 초기화
    }
    if (name === "robotName") {
      setIsRobotNameValid(value.length >= 2); // 추가된 상태 업데이트
    }
    if (name === "age") {
      const ageValid = /^[0-9]{1,3}$/.test(value) && value >= 0 && value <= 120;
      setIsAgeValid(ageValid); // 추가된 상태 업데이트
    }
  };

  const sendVerificationEmail = async () => {
    try {
      const response = await axios.post(
        `${localhostUrl}/email/verification`,
        null,
        {
          params: { email: formData.email },
        }
      );
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
      const response = await axios.get(`${localhostUrl}/email/verification`, {
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

  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const toggleShowConfirmPassword = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  const nextStep = () => {
    if (formData.password !== formData.confirmPassword) {
      setPasswordsMatch(false);
      return;
    }
    setPasswordsMatch(true);
    setStep(step + 1);
  };

  const prevStep = () => {
    setStep(step - 1);
  };

  const handleSubmit = async () => {
    try {
      // 회원가입 요청

      await axios.post(`${localhostUrl}/user`, {
        userId: formData.userId,
        password: formData.password,
        name: formData.name,
        email: formData.email,
        phoneNumber: formData.phoneNumber,
        gender: formData.gender,
        age: formData.age,
      });

      // 로봇 정보 등록 요청
      await axios.post(`${localhostUrl}/robot`, {
        userId: formData.userId,
        robotSerialNumber: formData.robotSerialNumber,
        robotName: formData.robotName,
        robotStyle: formData.robotStyle,
        robotGender: formData.robotGender,
      });

      alert("회원가입 및 로봇 정보 등록이 완료되었습니다.");
      onHide();
    } catch (error) {
      console.error("회원가입 및 로봇 정보 등록 실패:", error);
      console.error(error.response.data);
      alert("회원가입 및 로봇 정보 등록에 실패했습니다. 다시 시도해주세요.");
    }
  };

  const handleVerifySerial = async () => {
    if (formData.robotSerialNumber.length === 0) {
      setIsSerialValid(false);
      setSerialVerificationResult("로봇 시리얼 번호를 입력해주세요.");
      return;
    }

    try {
      const response = await axios.get(`${localhostUrl}/robot/verify`, {
        params: { robotSerialNumber: formData.robotSerialNumber },
      });
      if (response.status === 200) {
        setIsSerialValid(true);
        setSerialVerificationResult("로봇 시리얼 번호 검증 성공");
      }
    } catch (error) {
      setIsSerialValid(false);
      if (error.response && error.response.status === 400) {
        setSerialVerificationResult("유효하지 않은 시리얼 번호");
      } else if (error.response.status === 409) {
        setSerialVerificationResult(
          "해당 시리얼 번호에 대한 회원과 로봇이 이미 존재합니다."
        );
      } else {
        setSerialVerificationResult("오류가 발생했습니다.");
      }
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
        backdrop="static"
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            {step === 1 ? "회원가입" : "로봇 정보"}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {step === 1 && (
            <Form>
              <Form.Group className="mb-3" controlId="formBasicUsername">
                <Form.Label>아이디</Form.Label>
                <InputGroup>
                  <Form.Control
                    type="text"
                    placeholder="아이디를 입력해주세요"
                    name="userId"
                    value={formData.userId}
                    onChange={handleInputChange}
                    disabled={isUsernameLocked}
                  />
                  {!isUsernameLocked ? (
                    <Button
                      className="btn btn-main"
                      onClick={handleCheckUsername}
                      disabled={formData.userId.length < 3}
                    >
                      중복확인
                    </Button>
                  ) : (
                    <Button
                      className="btn btn-main"
                      onClick={handleResetUsername}
                    >
                      재설정
                    </Button>
                  )}
                </InputGroup>
                {usernameVerificationResult && (
                  <Form.Text
                    className={`text-${
                      isUsernameAvailable ? "success" : "danger"
                    }`}
                  >
                    {usernameVerificationResult}
                  </Form.Text>
                )}
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>비밀번호</Form.Label>
                <InputGroup>
                  <Form.Control
                    type={showPassword ? "text" : "password"}
                    placeholder="비밀번호를 입력해주세요"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                  />
                  <Button
                    className="btn btn-main"
                    variant="outline-secondary"
                    onClick={toggleShowPassword}
                  >
                    {showPassword ? <FaEyeSlash /> : <FaEye />}
                  </Button>
                </InputGroup>
                {!isPasswordValid && (
                  <Form.Text className="text-danger">
                    비밀번호는 8자 이상이어야 하며, 문자, 숫자, 특수문자를 모두
                    포함해야 합니다.
                  </Form.Text>
                )}
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicConfirmPassword">
                <Form.Label>비밀번호 확인</Form.Label>
                <InputGroup>
                  <Form.Control
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="비밀번호를 다시 입력해주세요"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                  />
                  <Button
                    className="btn btn-main"
                    variant="outline-secondary"
                    onClick={toggleShowConfirmPassword}
                  >
                    {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
                  </Button>
                </InputGroup>
                {!passwordsMatch && (
                  <Form.Text className="text-danger">
                    비밀번호가 일치하지 않습니다.
                  </Form.Text>
                )}
              </Form.Group>
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
                          인증 코드 유효 시간: {Math.floor(timer / 60)}:{timer % 60 < 10 ? `0${timer % 60}` : timer % 60}
                        </Form.Text>
                      )}
                    </div>
                  )}
                
              </Form.Group>

              {emailSent && (
                <Form.Group
                  className="mb-3"
                  controlId="formBasicVerificationCode"
                >
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
              <Form.Group className="mb-3" controlId="formBasicPhone">
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
                  <option value="">성별 선택</option>
                  <option value="남성">남성</option>
                  <option value="여성">여성</option>
                  <option value="기타">기타</option>
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
                    유효한 나이를 입력해주세요. (0-120)
                  </Form.Text>
                )}
              </Form.Group>
              <div
                style={{
                  width: "100%",
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <Button
                  className="btn btn-main"
                  onClick={nextStep}
                  disabled={!isVerified}
                  style={{ marginLeft: "auto" }}
                >
                  다음
                </Button>
              </div>
            </Form>
          )}
          {step === 2 && (
            <Form>
              <Form.Group className="mb-3" controlId="formBasicSerial">
                <Form.Label>로봇 시리얼 번호</Form.Label>
                <InputGroup>
                  <Form.Control
                    type="text"
                    placeholder="로봇 시리얼 번호를 입력해주세요"
                    name="robotSerialNumber"
                    value={formData.robotSerialNumber}
                    onChange={handleInputChange}
                  />
                  <Button className="btn btn-main" onClick={handleVerifySerial}>
                    인증
                  </Button>
                </InputGroup>
                {serialVerificationResult && (
                  <Form.Text
                    className={`text-${isSerialValid ? "success" : "danger"}`}
                  >
                    {serialVerificationResult}
                  </Form.Text>
                )}
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicRobotName">
                <Form.Label>로봇 이름</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="로봇 이름을 입력해주세요"
                  name="robotName"
                  value={formData.robotName}
                  onChange={handleInputChange}
                />
                {!isRobotNameValid && (
                  <Form.Text className="text-danger">
                    로봇 이름은 2자 이상이어야 합니다.
                  </Form.Text>
                )}
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicRobotStyle">
                <Form.Label>로봇 성격</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.robotStyle}
                  onChange={(e) =>
                    setFormData({ ...formData, robotStyle: e.target.value })
                  }
                >
                  <option value="">성격 선택</option>
                  <option value="친근">친근</option>
                  <option value="도도">도도</option>
                  <option value="활발">활발</option>
                  <option value="소심">소심</option>
                </Form.Control>
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicRobotGender">
                <Form.Label>로봇 성별</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.robotGender}
                  onChange={(e) =>
                    setFormData({ ...formData, robotGender: e.target.value })
                  }
                >
                  <option value="">성별 선택</option>
                  <option value="수컷">수컷</option>
                  <option value="암컷">암컷</option>
                </Form.Control>
              </Form.Group>
              <div
                style={{
                  width: "100%",
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <Button className="btn btn-main" onClick={prevStep}>
                  이전
                </Button>
                <Button
                  className="btn btn-main"
                  onClick={handleSubmit}
                  disabled={!isSerialValid || !isRobotNameValid}
                >
                  회원가입
                </Button>
              </div>
            </Form>
          )}
        </Modal.Body>
      </Modal>
    </Container>
  );
};

SignUpModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
};

export default SignUpModal;
