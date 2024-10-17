package ssafy.everpet.global.mqtt.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MqttUserDTO {
    private String userName;
    private String userID;
    private String userGender;
    private int userAge;
}
