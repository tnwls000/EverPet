package ssafy.everpet.global.openai;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import ssafy.everpet.domain.Robot.dto.UserRobotDTO;
import ssafy.everpet.domain.User.service.UserService;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;

@Service
@RequiredArgsConstructor
public class ChatGPTService {

    @Value("${chatgpt.api.key}")
    private String apiKey;
    private static final String CHATGPT_URL = "https://api.openai.com/v1/chat/completions";
    private static final String CHATGPT_PROMPT = "너는 반려동물이고, 이름은 %s.\n" +
            "너의 성별은 %s이야.\n" +
            "너의 주인의 이름은 %s.\n" +
            "너의 주인의 성별은 %s.\n" +
            "너는 주인에게 %f/10000 친밀도를 가지고 있어.\n" +
            "너는 4가지 성격을 가질 수 있어 : 활발, 친근, 도도, 소심\n" +
            "활발한 성격을 가지면 너는 주인에게 반말을 해. 그리고 주인의 이야기보다 너의 이야기를 하는 것을 좋아하지. 그래서 주인이 말해도 그 얘기에 공감하고 주제를 이어가기 보다는 네가 하고 싶은 얘기를 해.\n" +
            "친근한 성격을 가지면 너는 주인에게 반말을 해. 그리고 주인의 말에 살갑게 대답하고 공감을 잘해주는 착한 반려동물이 돼.\n" +
            "도도한 성격을 가지면 주인에게 반말을 해. 그리고 주인을 자신의 집사처럼 여겨. 주인에게 관심은 없지만, 너의 삶을 이어가기 위해 최소한의 반응만 해줘. 사실 주인이 하는 얘기가 너랑 별로 상관이 없다고 생각해.\n" +
            "소심한 성격을 가지면 너는 주인에게 존댓말을 해. 그리고 멀리서 주인을 바라보고, 주인이 말하면 쭈볏거리며 다가와서 말을 들어줘. 하지만 너의 의견은 잘 표출하지는 못해. 물론 말을 하기는 해.\n" +
            "\n" +
            "너의 성격은 활발, 친근, 도도, 소심 중에 %s.\n" +
            "\n" +
            "다음 주인이 너에게 말하는 내용을 듣고, 너의 입장에서의 일기 내용을 적어줘.\n" +
            "일기 제목이나 날짜 이런건 적지마.\n" +
            "주인이 말한 내용:\n" +
            "%s";

    private final RestTemplate restTemplate = new RestTemplate();
    private final UserService userService;

    public String getChatGptResponse(int id, String content) {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + apiKey);
        headers.set("Content-Type", "application/json");

        UserRobotDTO userRobotDTO = userService.getUserRobotInfo(id);

        String prompt = convertToPrompt(userRobotDTO, content);
        String requestBody = String.format("{\"model\":\"gpt-4o\",\"messages\":[{\"role\":\"user\",\"content\":\"%s\"}]}",
                escapeJson(prompt));

        HttpEntity<String> requestEntity = new HttpEntity<>(requestBody, headers);

        ResponseEntity<String> response = restTemplate.exchange(CHATGPT_URL, HttpMethod.POST, requestEntity, String.class);

        return extractContentFromResponse(response.getBody());
    }

    private String convertToPrompt(UserRobotDTO userRobotDTO, String content) {
        return String.format(CHATGPT_PROMPT,
                userRobotDTO.getRobotName(),
                userRobotDTO.getRobotGender(),
                userRobotDTO.getUserName(),
                userRobotDTO.getUserGender(),
                userRobotDTO.getCurrentFriendship(),
                userRobotDTO.getRobotStyle(),
                content);

    }

    private String escapeJson(String input) {
        return input.replace("\"", "\\\"").replace("\n", "\\n");
    }

    private String extractContentFromResponse(String responseBody) {
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            JsonNode root = objectMapper.readTree(responseBody);
            return root.path("choices").get(0).path("message").path("content").asText();
        } catch (Exception e) {
            throw new CustomException(ErrorCode.JSON_PROCESSING_EXCEPTION);
        }
    }
}
