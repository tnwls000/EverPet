package ssafy.everpet.domain.Diary.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class DiarySaveDTO {
    private String userId;
    private String content;
    private String imageUrl;
}
