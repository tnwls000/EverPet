package ssafy.everpet.global.mqtt.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MqttUserIdSerialNumberDTO {
    private String userId;
    private String serialNumber;
}
