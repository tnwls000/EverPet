package ssafy.everpet.domain.User.service;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import ssafy.everpet.domain.User.dto.EmailDTO;

import java.util.Random;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class EmailService {

    private final JavaMailSender mailSender;

    public void sendVerificationEmail(EmailDTO emailDTO) throws MessagingException {
        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, "UTF-8");

        helper.setFrom("everpetcompany@naver.com");
        helper.setTo(emailDTO.getToEmail());
        helper.setSubject(emailDTO.getSubject());
        helper.setText(emailDTO.getBody() + emailDTO.getCode(), true);

        mailSender.send(message);
    }

    public String generateVerificationCode() {
        return UUID.randomUUID().toString().substring(0, 6);
    }
}
