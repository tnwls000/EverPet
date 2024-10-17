package ssafy.everpet.global.mqtt.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;
import ssafy.everpet.domain.AccessLog.service.AccessLogService;
import ssafy.everpet.domain.Map.dto.MapSaveDTO;
import ssafy.everpet.domain.Map.service.MapService;
import ssafy.everpet.domain.Robot.dto.RobotInfoDTO;
import ssafy.everpet.domain.Robot.dto.UserRobotDTO;
import ssafy.everpet.domain.Robot.service.RobotService;
import ssafy.everpet.domain.User.dto.UserInfoDTO;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;
import ssafy.everpet.global.mqtt.dto.*;

import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Service
@Slf4j
@RequiredArgsConstructor
public class MqttService implements MqttCallback {

    @Value("${MQTT_BROKER_HOST}")
    private String host;

    @Value("${MQTT_BROKER_PORT}")
    private int port;

    private static final String IN = "IN";
    private static final String OUT = "OUT";
    private static final String ACCESS_LOG_IN_TOPIC = "web/doorEnter/In";
    private static final String ACCESS_LOG_OUT_TOPIC = "web/doorEnter/Out";
    private static final String FRIENDSHIP_TOPIC = "web/friendship";
    private static final String MAP_SAVE_TOPIC = "web/map";
    private static final String MAP_CONFIRM_TOPIC = "web/mapConfirm";

    private MqttClient client;
    private final AccessLogService accessLogService;
    private final RobotService robotService;
    private final MapService mapService;

    @PostConstruct
    public void connect() {
        String serverURI = getURI();
        String uuid = UUID.randomUUID().toString();

        log.info("MQTT Broker Server: {}", serverURI);
        log.info("UUID: {}", uuid);

        MqttConnectOptions option = new MqttConnectOptions();
        option.setAutomaticReconnect(true);
        option.setKeepAliveInterval(60);
        option.setCleanSession(true);
        option.setMaxReconnectDelay(1000); // 최대 재연결 지연을 1초로 설정
        option.setConnectionTimeout(10);  // 연결 타임아웃을 10초로 설정


        try {
            client = new MqttClient(serverURI, uuid, new MemoryPersistence());
            client.setCallback(this);
            client.connect(option);

            subscribe("+/" + ACCESS_LOG_IN_TOPIC);
            subscribe("+/" + ACCESS_LOG_OUT_TOPIC);
            subscribe("+/" + FRIENDSHIP_TOPIC);
            subscribe("+/" + MAP_SAVE_TOPIC);
            subscribe("+/" + MAP_CONFIRM_TOPIC);
        } catch (MqttException e) {
            log.info("MQTT Connection Error : {}", e.getMessage());
        }
    }

    private String getURI() {
        return "tcp://" + host + ":" + port;
    }

    public void publish(MqttMessageDTO mqttMessageDTO) {
        log.info("Message is published : {} / {}", mqttMessageDTO.getTopic(), mqttMessageDTO.getMessage());

        MqttMessage message = new MqttMessage();
        try {
            message.setPayload(mqttMessageDTO.getMessage().getBytes(StandardCharsets.UTF_8));
            client.publish(mqttMessageDTO.getTopic(),message);
        } catch(Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
    }

    public String getJsonOfAllInfo(UserRobotDTO userRobotDTO, int initFriendship) {
        ObjectMapper objectMapper = new ObjectMapper();

        MqttUserDTO user = MqttUserDTO.builder()
                .userName(userRobotDTO.getUserName())
                .userID(userRobotDTO.getUserID())
                .userGender(userRobotDTO.getUserGender())
                .userAge(userRobotDTO.getUserAge())
                .build();

        MqttRobotDTO robot = MqttRobotDTO.builder()
                .name(userRobotDTO.getRobotName())
                .personality(userRobotDTO.getRobotStyle())
                .gender(userRobotDTO.getRobotGender())
                .serialNumber(userRobotDTO.getSerialNumber())
                .build();

        MqttInteractionDTO interaction = MqttInteractionDTO.builder()
                .diaryContinuity(0)
                .build();

        MqttFriendshipDTO friendship = MqttFriendshipDTO.builder()
                .current(initFriendship)
                .build();

        MqttAllInfoDTO allInfo = MqttAllInfoDTO.builder()
                .user(user)
                .robot(robot)
                .interaction(interaction)
                .friendship(friendship)
                .build();
        String message = "";
        try {
            message = objectMapper.writeValueAsString(allInfo);
        } catch (JsonProcessingException e) {
            throw new CustomException(ErrorCode.JSON_PROCESSING_EXCEPTION);
        }
        return message;
    }

    public String getJsonOfUser(UserInfoDTO userInfoDTO) {
        ObjectMapper objectMapper = new ObjectMapper();

        MqttUserDTO user = MqttUserDTO.builder()
                .userName(userInfoDTO.getName())
                .userID(userInfoDTO.getUserId())
                .userGender(userInfoDTO.getGender())
                .userAge(userInfoDTO.getAge())
                .build();

        Map<String, Object> userMessage = new HashMap<>();
        userMessage.put("user", user);

        String message = "";
        try {
            message = objectMapper.writeValueAsString(userMessage);
        } catch (JsonProcessingException e) {
            throw new CustomException(ErrorCode.JSON_PROCESSING_EXCEPTION);
        }
        return message;
    }

    public String getJsonOfRobot(RobotInfoDTO robotInfoDTO) {
        ObjectMapper objectMapper = new ObjectMapper();

        MqttRobotDTO robot = MqttRobotDTO.builder()
                .name(robotInfoDTO.getRobotName())
                .personality(robotInfoDTO.getRobotStyle())
                .gender(robotInfoDTO.getRobotGender())
                .serialNumber(robotInfoDTO.getRobotSerialNumber())
                .build();

        Map<String, Object> robotMessage = new HashMap<>();
        robotMessage.put("robot", robot);

        String message = "";
        try {
            message = objectMapper.writeValueAsString(robotMessage);
        } catch (JsonProcessingException e) {
            throw new CustomException(ErrorCode.JSON_PROCESSING_EXCEPTION);
        }
        return message;
    }

    public String getJsonOfUserIdAndSerialNumber(String userId, String serialNumber) {
        ObjectMapper objectMapper = new ObjectMapper();

        MqttUserIdSerialNumberDTO userIdSerialNumberDTO = MqttUserIdSerialNumberDTO.builder()
                .userId(userId)
                .serialNumber(serialNumber)
                .build();

        String message = "";
        try {
            message = objectMapper.writeValueAsString(userIdSerialNumberDTO);
        } catch (JsonProcessingException e) {
            throw new CustomException(ErrorCode.JSON_PROCESSING_EXCEPTION);
        }
        return message;
    }

    public void subscribe(String topic) {
        try {
            client.subscribe(topic);
            log.info("subscribe topic : {}", topic);
        } catch (MqttException e) {
            log.error("Subscription error: {}", e.getMessage());
        }
    }

    @Override
    public void connectionLost(Throwable throwable) {

        log.error("Connection lost: {}", throwable.getMessage());
        try {
            client.reconnect();
        } catch (MqttException e) {
            log.error("Reconnection failed: {}", e.getMessage());
        }
    }

    @Override
    public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
        log.info(topic + " 받음");
        String message = new String(mqttMessage.getPayload(), StandardCharsets.UTF_8);
        String userId = message.split("/")[0];
        if (topic.matches("^.+/"+ACCESS_LOG_IN_TOPIC+"$")) {
            LocalDateTime accessTime = LocalDateTime.parse(message.split("/")[1]);
            accessLogService.saveAccessLog(userId, accessTime, IN);
        }
        if (topic.matches("^.+/"+ACCESS_LOG_OUT_TOPIC+"$")) {
            LocalDateTime accessTime = LocalDateTime.parse(message.split("/")[1]);
            accessLogService.saveAccessLog(userId, accessTime, OUT);
        }
        if (topic.matches("^.+/"+FRIENDSHIP_TOPIC+"$")) {
            double friendship = Double.parseDouble(message.split("/")[1]);
            robotService.updateCurrentFriendship(userId, friendship);
        }
        if (topic.matches("^.+/"+ MAP_SAVE_TOPIC +"$") || topic.matches("^.+/"+ MAP_CONFIRM_TOPIC +"$")) {
            String mapJson = message.split("/")[1];
            MapSaveDTO mapSaveDTO = convertToMapSaveDTO(userId, mapJson);
            mapService.saveOrUpdateMap(mapSaveDTO);
        }
    }

    private MapSaveDTO convertToMapSaveDTO(String userId, String mapJson) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        JsonNode mapNode = objectMapper.readTree(mapJson);

        JsonNode mapDataNode = mapNode.path("data");
        JsonNode infoNode = mapNode.path("info");
        JsonNode originNode = infoNode.path("origin");

         return MapSaveDTO.builder()
                .userId(userId)
                .width(infoNode.path("width").asInt())
                .height(infoNode.path("height").asInt())
                .resolution(infoNode.path("resolution").asDouble())
                .data(parseData(mapDataNode))
                .positionX(originNode.path("position").path("x").asDouble())
                .positionY(originNode.path("position").path("y").asDouble())
                .positionZ(originNode.path("position").path("z").asDouble())
                .orientationX(originNode.path("orientation").path("x").asDouble())
                .orientationY(originNode.path("orientation").path("y").asDouble())
                .orientationZ(originNode.path("orientation").path("z").asDouble())
                .orientationW(originNode.path("orientation").path("w").asDouble())
                .build();
    }

    private short[] parseData(JsonNode dataNode) {
        if (dataNode.isArray()) {
            short[] shortArray = new short[dataNode.size()];
            for (int i = 0; i < dataNode.size(); i++) {
                shortArray[i] = (short) dataNode.get(i).asInt();
            }
            return shortArray;
        } else {
            throw new IllegalArgumentException("JsonNode is not an array");
        }
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
        log.info("Delivery complete: {}", iMqttDeliveryToken.isComplete());
    }
}
