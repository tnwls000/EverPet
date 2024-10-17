package ssafy.everpet.domain.User.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
@AllArgsConstructor
public class UserFindPasswordDTO {
    private String userId;
    private String email;
}