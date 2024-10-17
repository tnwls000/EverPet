package ssafy.everpet.domain.User.controller;

import jakarta.mail.MessagingException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ssafy.everpet.domain.User.dto.EmailDTO;
import ssafy.everpet.domain.User.service.EmailService;
import ssafy.everpet.domain.User.service.UserService;
import ssafy.everpet.global.util.RedisUtil;

@RestController
@RequestMapping("/email/verification")
@RequiredArgsConstructor
public class EmailController {

    private final UserService userService;
    private final EmailService emailService;
    private final RedisUtil redisUtil;

    private static final String VERIFICATION_SUBJECT = "에버펫: 회원가입 인증 코드 발송 이메일입니다.";
    private static final String VERIFICATION_BODY = "에버펫을 방문해주셔서 감사합니다.<br>아래의 인증번호를 인증번호 확인란에 기입해주시기 바랍니다.<br>인증번호 : ";
    private static final Long VERIFICATION_TIMEOUT = 60*3L;

    @PostMapping
    public ResponseEntity<String> sendVerificationCode(@RequestParam String email) throws MessagingException {
        userService.checkEmailDuplication(email);

        String code = emailService.generateVerificationCode();
        EmailDTO emailDTO = EmailDTO.builder()
                .toEmail(email)
                .code(code)
                .subject(VERIFICATION_SUBJECT)
                .body(VERIFICATION_BODY)
                .build();
        emailService.sendVerificationEmail(emailDTO);

        redisUtil.setDataExpire(code, email, VERIFICATION_TIMEOUT);

        return ResponseEntity.status(HttpStatus.OK).body("이메일 인증 코드 전송 성공");
    }

    @GetMapping
    public ResponseEntity<String> checkVerificationCode(@RequestParam String verificationCode) {
        if (redisUtil.hasKey(verificationCode)) return ResponseEntity.status(HttpStatus.OK).body("코드 인증 성공");
        else return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("코드 인증 실패");
    }
}