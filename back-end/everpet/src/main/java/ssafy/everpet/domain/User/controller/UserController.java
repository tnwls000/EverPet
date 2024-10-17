package ssafy.everpet.domain.User.controller;

import jakarta.mail.MessagingException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import ssafy.everpet.domain.Friendship.service.FriendshipService;
import ssafy.everpet.domain.Robot.dto.RobotInfoDTO;
import ssafy.everpet.domain.Robot.dto.UserRobotDTO;
import ssafy.everpet.domain.Robot.service.RobotService;
import ssafy.everpet.domain.User.dto.*;
import ssafy.everpet.domain.User.entity.CustomUserDetails;
import ssafy.everpet.domain.User.entity.User;
import ssafy.everpet.domain.User.service.EmailService;
import ssafy.everpet.domain.User.service.UserService;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;
import ssafy.everpet.global.mqtt.dto.MqttMessageDTO;
import ssafy.everpet.global.mqtt.service.MqttService;
import ssafy.everpet.global.util.JwtTokenUtil;
import ssafy.everpet.global.util.PasswordUtil;

import java.util.Collections;
import java.util.Map;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping("/user")
public class UserController {

    private final UserService userService;
    private final EmailService emailService;
    private final JwtTokenUtil jwtTokenUtil;
    private final PasswordEncoder passwordEncoder;
    private final MqttService mqttService;

    private static final String FIND_PASSWORD_SUBJECT = "에버펫: 임시 비밀번호 발송 이메일입니다.";
    private static final String FIND_PASSWORD_BODY = "님, 안녕하세요<br>에버펫 임시 비밀번호 발급 관련 이메일입니다.<br><br>임시 비밀번호로 로그인 후 꼭 비밀번호를 변경하시기 바랍니다.<br><br>임시 비밀번호 : ";

    @PostMapping
    public ResponseEntity<String> signUp(@RequestBody UserSignUpDTO userSignUpDTO) {
        userService.signUp(userSignUpDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body("회원가입 성공");
    }

    @GetMapping("/validate-id")
    public ResponseEntity<String> validateId(@RequestParam String userId) {
        userService.validateUserId(userId);
        return ResponseEntity.status(HttpStatus.OK).body("아이디 중복 확인 성공");
    }

    @PostMapping("/login")
    public ResponseEntity<String> login(HttpServletResponse response, @RequestBody UserLoginDTO userLoginDTO) {
        int id = userService.login(userLoginDTO);

        String accessToken = jwtTokenUtil.createAccessToken(id);
        jwtTokenUtil.sendAccessToken(response, accessToken);

        String refreshToken = jwtTokenUtil.createRefreshToken(id);
        jwtTokenUtil.sendRefreshToken(id, refreshToken);
        return ResponseEntity.status(HttpStatus.OK).body("로그인 성공");
    }

    @GetMapping
    public ResponseEntity<UserInfoDTO> getUserInfo(@AuthenticationPrincipal CustomUserDetails customUserDetails) {
        int id = customUserDetails.getId();
        UserInfoDTO userInfo = userService.getUserInfo(id);
        return new ResponseEntity<>(userInfo, HttpStatus.OK);
    }

    @PatchMapping
    public ResponseEntity<String> updateUser(@AuthenticationPrincipal CustomUserDetails customUserDetails,
                                             @RequestBody UserUpdateDTO userUpdateDTO) {
        int id = customUserDetails.getId();
        userService.modifyUser(id, userUpdateDTO);
        UserInfoDTO userInfoDTO = userService.getUserInfo(id);

        UserRobotDTO userRobotInfo = userService.getUserRobotInfo(id);
        mqttPublish(userInfoDTO, userRobotInfo.getSerialNumber(), "/raspberry/modify/user");

        return ResponseEntity.status(HttpStatus.CREATED).body("회원 수정 성공");
    }

    private void mqttPublish(UserInfoDTO userInfoDTO, String serialNumber, String topic) {
        String json = mqttService.getJsonOfUser(userInfoDTO);
        MqttMessageDTO mqttMessageDTO = MqttMessageDTO.builder()
                .topic(serialNumber + topic)
                .message(json)
                .build();

        mqttService.publish(mqttMessageDTO);
    }

    @DeleteMapping
    public ResponseEntity<String> deleteUser(@AuthenticationPrincipal CustomUserDetails customUserDetails,
                                             @RequestParam String password) {
        int id = customUserDetails.getId();
        userService.deleteUser(id, password);
        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }

    @PostMapping("/logout")
    public ResponseEntity<String> logout(HttpServletRequest request, @AuthenticationPrincipal CustomUserDetails customUserDetails) {
        String accessToken = jwtTokenUtil.extractAccessToken(request).orElseThrow(() -> new CustomException(ErrorCode.JWT_NOT_FOUND_ACCESS_TOKEN));
        int id = customUserDetails.getId();
        userService.logout(id, accessToken);
        return ResponseEntity.status(HttpStatus.OK).body("로그아웃 성공");
    }

    @GetMapping("/find-id")
    public ResponseEntity<Map<String,String>> findId(@RequestParam("name") String name, @RequestParam("email") String email) {
        UserFindIdDTO userFindIdDTO = UserFindIdDTO.builder()
                .name(name)
                .email(email)
                .build();
        String id = userService.findId(userFindIdDTO);

        return ResponseEntity.status(HttpStatus.OK).body(Collections.singletonMap("userId", id));
    }

    @PostMapping("/find-password")
    @Transactional
    public ResponseEntity<String> findPassword(@RequestBody UserFindPasswordDTO userFindPasswordDTO) throws MessagingException {
        User user = userService.findPassword(userFindPasswordDTO);
        String temporalPassword = PasswordUtil.generateRandomPassword();

        EmailDTO emailDTO = EmailDTO.builder()
                        .toEmail(user.getEmail())
                        .code(temporalPassword)
                        .subject(FIND_PASSWORD_SUBJECT)
                        .body(user.getName()+FIND_PASSWORD_BODY)
                        .build();
        emailService.sendVerificationEmail(emailDTO);
        user.updatePassword(passwordEncoder.encode(temporalPassword));

        return ResponseEntity.status(HttpStatus.OK).body("임시 비밀번호 전송 성공");
    }
}
