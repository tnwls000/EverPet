package ssafy.everpet.domain.Robot.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class RobotInfoDTO {
    private String robotSerialNumber;
    private String robotName;
    private String robotStyle;
    private String robotGender;
}
