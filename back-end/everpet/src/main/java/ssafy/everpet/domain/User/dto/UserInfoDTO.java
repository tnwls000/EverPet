package ssafy.everpet.domain.User.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class UserInfoDTO {
    private String userId;
    private String name;
    private String email;
    private String phoneNumber;
    private String gender;
    private int age;
}
