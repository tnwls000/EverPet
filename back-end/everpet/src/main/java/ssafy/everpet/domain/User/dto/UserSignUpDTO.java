package ssafy.everpet.domain.User.dto;

import lombok.*;

@Getter
@AllArgsConstructor
@NoArgsConstructor
public class UserSignUpDTO {
    private String userId;
    private String password;
    private String name;
    private String email;
    private String phoneNumber;
    private String gender;
    private int age;
}
