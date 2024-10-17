package ssafy.everpet.domain.Robot.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import ssafy.everpet.domain.Friendship.service.FriendshipService;
import ssafy.everpet.domain.Robot.dto.RobotInfoDTO;
import ssafy.everpet.domain.Robot.dto.RobotSaveDTO;
import ssafy.everpet.domain.Robot.dto.RobotUpdateDTO;
import ssafy.everpet.domain.Robot.dto.UserRobotDTO;
import ssafy.everpet.domain.Robot.service.RobotService;
import ssafy.everpet.domain.User.entity.CustomUserDetails;
import ssafy.everpet.global.mqtt.dto.*;
import ssafy.everpet.global.mqtt.service.MqttService;

@RestController
@RequestMapping("/robot")
@RequiredArgsConstructor
public class RobotController {

    private final RobotService robotService;
    private final MqttService mqttService;
    private final FriendshipService friendshipService;

    @PostMapping
    public ResponseEntity<String> addRobot(@RequestBody RobotSaveDTO robotSaveDTO) {
        UserRobotDTO userRobotDTO = robotService.saveRobot(robotSaveDTO);
        mqttPublishToRP(userRobotDTO);
        mqttPublishToJS(userRobotDTO.getUserID(), userRobotDTO.getSerialNumber());

        return ResponseEntity.status(HttpStatus.CREATED).body("로봇 저장 성공");
    }

    @GetMapping
    public ResponseEntity<RobotInfoDTO> getRobotInfo(@AuthenticationPrincipal CustomUserDetails customUserDetails) {
        int id = customUserDetails.getId();
        RobotInfoDTO robotInfoDTO = robotService.getRobotInfoByUserId(id);
        return new ResponseEntity<>(robotInfoDTO, HttpStatus.OK);
    }

    @PatchMapping
    public ResponseEntity<String> updateRobot(@AuthenticationPrincipal CustomUserDetails customUserDetails,
                                              @RequestBody RobotUpdateDTO robotUpdateDTO) {
        int id = customUserDetails.getId();
        robotService.modifyRobot(id, robotUpdateDTO);
        RobotInfoDTO robotInfoDTO = robotService.getRobotInfoByUserId(id);
        mqttPublishToRP(robotInfoDTO);

        return ResponseEntity.status(HttpStatus.OK).body("로봇 수정 성공");
    }

    private void mqttPublishToRP(UserRobotDTO userRobotDTO) {
        int initFriendship = friendshipService.findInitFriendshipByTypeStyle(userRobotDTO.getRobotStyle());
        String json = mqttService.getJsonOfAllInfo(userRobotDTO, initFriendship);

        MqttMessageDTO mqttMessageDTO = MqttMessageDTO.builder()
                .topic(userRobotDTO.getSerialNumber() + "/raspberry/allinfo")
                .message(json)
                .build();
        mqttService.publish(mqttMessageDTO);
    }

    private void mqttPublishToRP(RobotInfoDTO robotInfoDTO) {
        String json = mqttService.getJsonOfRobot(robotInfoDTO);

        MqttMessageDTO mqttMessageDTO = MqttMessageDTO.builder()
                .topic(robotInfoDTO.getRobotSerialNumber() + "/raspberry/modify/robot")
                .message(json)
                .build();
        mqttService.publish(mqttMessageDTO);
    }

    private void mqttPublishToJS(String userId, String serialNumber) {
        String json = mqttService.getJsonOfUserIdAndSerialNumber(userId, serialNumber);

        MqttMessageDTO mqttMessageDTO = MqttMessageDTO.builder()
                .topic(serialNumber + "/jetson/userId")
                .message(json)
                .build();
        mqttService.publish(mqttMessageDTO);
    }

    @GetMapping("/verify")
    public ResponseEntity<String> verifySerialNumber(@RequestParam String robotSerialNumber) {
        robotService.verifySerialNumber(robotSerialNumber);
        return ResponseEntity.status(HttpStatus.OK).body("기기 번호 검증 성공");
    }
}
