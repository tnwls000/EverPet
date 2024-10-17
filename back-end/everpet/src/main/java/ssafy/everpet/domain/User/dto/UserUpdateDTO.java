package ssafy.everpet.domain.User.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class UserUpdateDTO {
    private String name;
    private String password;
    private String newPassword;
    private String email;
    private String phoneNumber;
    private String gender;
    private int age;
}
