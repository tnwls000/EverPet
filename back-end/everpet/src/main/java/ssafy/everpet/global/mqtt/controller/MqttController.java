package ssafy.everpet.global.mqtt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import ssafy.everpet.global.mqtt.dto.MqttMessageDTO;
import ssafy.everpet.global.mqtt.service.MqttService;

@RestController
@RequiredArgsConstructor
@RequestMapping("/mqtt")
public class MqttController {

    private final MqttService mqttService;

    @PostMapping("/publish")
    public ResponseEntity<String> publishMessage(@RequestBody MqttMessageDTO request) {
        mqttService.publish(request);
        return ResponseEntity.ok().body(request.getTopic() + " topic published");
    }
}

