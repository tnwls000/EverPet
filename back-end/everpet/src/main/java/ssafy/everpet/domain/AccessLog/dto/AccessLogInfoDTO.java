package ssafy.everpet.domain.AccessLog.dto;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class AccessLogInfoDTO {
    private int accessId;
    private LocalDateTime accessTime;
    private String accessType;
}
