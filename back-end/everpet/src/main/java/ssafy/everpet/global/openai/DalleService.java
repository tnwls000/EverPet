package ssafy.everpet.global.openai;

import com.amazonaws.util.IOUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import ssafy.everpet.domain.User.dto.UserInfoDTO;


import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@Service
@Slf4j
public class DalleService {

    @Value("${openai.api.key}")
    private String apiKey;

    private static final String OPENAI_FILE_NAME = "generated_image.jpg";
    private static final String PROMPT =
            "내 이름은 %s. 내 성별은 %s. 내 나이는 %d세. 내가 일기를 썼어. 너는 크레파스로 그림을 그려주는 7살짜리 꼬마야. 내 일기 내용을 나타내는 그림을 귀엽게 그려줘. 너가 그린 그림을 보여줘. 내 일기 내용: %s";

    public MultipartFile generateImage(UserInfoDTO userInfoDTO, String content) throws Exception {
        String prompt = String.format(PROMPT, userInfoDTO.getName(), userInfoDTO.getGender(), userInfoDTO.getAge(), content);

        String url = "https://api.openai.com/v1/images/generations";
        String requestBody = String.format(
                "{\"model\":\"dall-e-3\",\"prompt\":\"%s\",\"n\":1,\"size\":\"1024x1024\"}",
                prompt);

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + apiKey)
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        String responseBody = response.body();
        String imageUrl = extractImageUrl(responseBody);
        byte[] imageBytes = downloadImage(imageUrl);

        return convertToMultipartFile(imageBytes);
    }

    private String extractImageUrl(String responseBody) {
        int startIndex = responseBody.indexOf("https://");
        int endIndex = responseBody.indexOf("\"", startIndex);
        return responseBody.substring(startIndex, endIndex);
    }

    private byte[] downloadImage(String imageUrl) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(imageUrl))
                .build();

        HttpResponse<InputStream> response = client.send(request, HttpResponse.BodyHandlers.ofInputStream());
        InputStream inputStream = response.body();
        return IOUtils.toByteArray(inputStream);
    }

    private MultipartFile convertToMultipartFile(byte[] imageBytes) throws IOException {
        ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(imageBytes);
        return new MockMultipartFile(OPENAI_FILE_NAME, "generated_image.jpg", "image/jpeg", byteArrayInputStream);
    }
}