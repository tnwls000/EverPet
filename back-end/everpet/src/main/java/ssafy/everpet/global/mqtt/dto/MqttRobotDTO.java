package ssafy.everpet.global.mqtt.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MqttRobotDTO {
    private String name;
    private String personality;
    private String gender;
    private String serialNumber;
}
