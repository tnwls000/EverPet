package ssafy.everpet.global.mqtt.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class MqttMessageDTO {
    private String topic;
    private String message;
}
