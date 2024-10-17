package ssafy.everpet.global.mqtt.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MqttAllInfoDTO {
    private MqttUserDTO user;
    private MqttRobotDTO robot;
    private MqttInteractionDTO interaction;
    private MqttFriendshipDTO friendship;
}
