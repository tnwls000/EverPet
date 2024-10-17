package ssafy.everpet.domain.User.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@AllArgsConstructor
@Getter
public class UserLoginDTO {
    private String userId;
    private String password;
}
