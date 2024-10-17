package ssafy.everpet.domain.Robot.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class UserRobotDTO {
    private String userName;
    private String userID;
    private String userGender;
    private int userAge;

    private String robotName;
    private String robotStyle;
    private String robotGender;
    private double currentFriendship;

    private String serialNumber;
}
