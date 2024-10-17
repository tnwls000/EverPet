package ssafy.everpet.domain.Diary.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.web.multipart.MultipartFile;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class DiaryRasberrySaveDTO {
    private String userId;
    private MultipartFile file;
    private String content;
}
