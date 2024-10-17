package ssafy.everpet.domain.User.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class EmailDTO {
    private String toEmail;
    private String code;
    private String subject;
    private String body;
}
