package ssafy.everpet.domain.Diary.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import ssafy.everpet.domain.Diary.dto.*;
import ssafy.everpet.domain.Diary.service.DiaryService;
import ssafy.everpet.domain.Robot.dto.RobotInfoDTO;
import ssafy.everpet.domain.Robot.service.RobotService;
import ssafy.everpet.domain.User.dto.UserInfoDTO;
import ssafy.everpet.domain.User.entity.CustomUserDetails;
import ssafy.everpet.domain.User.entity.User;
import ssafy.everpet.domain.User.service.UserService;
import ssafy.everpet.global.mqtt.dto.MqttMessageDTO;
import ssafy.everpet.global.mqtt.service.MqttService;
import ssafy.everpet.global.openai.ChatGPTService;
import ssafy.everpet.global.openai.DalleService;
import ssafy.everpet.global.s3.S3Service;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/diary")
@RequiredArgsConstructor
public class DiaryController {
    private final UserService userService;
    private final DiaryService diaryService;
    private final DalleService dalleService;
    private final S3Service s3Service;
    private final ChatGPTService chatGPTService;

    private final RobotService robotService;
    private final MqttService mqttService;

    private static final String DIARY_SAVE_TOPIC = "/raspberry";
    private static final String DIARY_SAVE_MESSAGE = "webDiaryDone";

    @PostMapping
    public ResponseEntity<String> saveDiaryFromFront(@AuthenticationPrincipal CustomUserDetails customUserDetails,
            @RequestBody DiaryFrontSaveDTO diaryFrontSaveDTO) throws Exception {
        String userId = customUserDetails.getUserId();
        int id = customUserDetails.getId();
        UserInfoDTO userInfoDTO = userService.getUserInfo(id);

        MultipartFile multipartFile = dalleService.generateImage(userInfoDTO, diaryFrontSaveDTO.getContent());
        String url = s3Service.uploadDiaryImage(multipartFile);

        String chatGptContent = chatGPTService.getChatGptResponse(id, diaryFrontSaveDTO.getContent());

        DiarySaveDTO diarySaveDTO = DiarySaveDTO.builder()
                        .content(chatGptContent)
                        .imageUrl(url)
                        .userId(userId)
                        .build();
        diaryService.saveDiary(userId, diarySaveDTO);

        RobotInfoDTO robotInfoDTO = robotService.getRobotInfoByUserId(id);
        MqttMessageDTO mqttMessageDTO = MqttMessageDTO.builder()
                .topic(robotInfoDTO.getRobotSerialNumber() + DIARY_SAVE_TOPIC)
                .message(DIARY_SAVE_MESSAGE)
                .build();
        mqttService.publish(mqttMessageDTO);

        return ResponseEntity.status(HttpStatus.OK).body("다이어리 저장 성공 from Front: " + url);
    }

    @PostMapping("/raspberry")
    public ResponseEntity<String> saveDiaryFromRaspberry(@RequestParam("content") String content,
                                                        @RequestParam("userId") String userId,
                                                        @RequestParam("image") MultipartFile image) throws IOException {
        String url = s3Service.uploadDiaryImage(image);
        User user = userService.getUserInfoByUserId(userId);
        String chatGptContent = chatGPTService.getChatGptResponse(user.getId(), content);

        DiarySaveDTO diarySaveDTO = DiarySaveDTO.builder()
                .content(chatGptContent)
                .imageUrl(url)
                .userId(userId)
                .build();
        diaryService.saveDiary(userId, diarySaveDTO);
        return ResponseEntity.status(HttpStatus.OK).body("다이어리 저장 성공 from Rasberry: " + url);
    }

    @GetMapping
    public ResponseEntity<List<DiaryInfoDTO>> getDiaries(@AuthenticationPrincipal CustomUserDetails customUserDetails) {
        int id = customUserDetails.getId();
        List<DiaryInfoDTO> diaries = diaryService.getDiaries(id);
        return new ResponseEntity<>(diaries, HttpStatus.OK);
    }

    @GetMapping("/{diaryId}")
    public ResponseEntity<DiaryInfoDTO> getDiary(@AuthenticationPrincipal CustomUserDetails customUserDetails,
                                                 @PathVariable("diaryId") int diaryId) {
        int id = customUserDetails.getId();
        DiaryInfoDTO diary = diaryService.getDiary(id, diaryId);
        return new ResponseEntity<>(diary, HttpStatus.OK);
    }

    @PatchMapping("/{diaryId}")
    public ResponseEntity<String> modifyDiary(@AuthenticationPrincipal CustomUserDetails customUserDetails,
                                              @PathVariable("diaryId") int diaryId,
                                              @RequestBody DiaryUpdateDTO diaryUpdateDTO) {
        int id = customUserDetails.getId();
        diaryService.modifyDiary(id, diaryId, diaryUpdateDTO);

        return ResponseEntity.status(HttpStatus.OK).body("다이어리 수정 성공");
    }

    @DeleteMapping("/{diaryId}")
    public ResponseEntity<String> deleteDiary(@AuthenticationPrincipal CustomUserDetails customUserDetails,
                                              @PathVariable("diaryId") int diaryId) {
        int id = customUserDetails.getId();
        diaryService.deleteDiary(id, diaryId);
        return ResponseEntity.status(HttpStatus.OK).body("다이어리 삭제 성공");
    }
}
