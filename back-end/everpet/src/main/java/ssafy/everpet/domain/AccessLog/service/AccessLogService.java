package ssafy.everpet.domain.AccessLog.service;

import ssafy.everpet.domain.AccessLog.dto.AccessLogInfoDTO;

import java.time.LocalDateTime;
import java.util.List;

public interface AccessLogService {
    List<AccessLogInfoDTO> getAccessLogs(String userId, String accessType, LocalDateTime startDate, LocalDateTime endDate);
    void saveAccessLog(String userId, LocalDateTime accessTime, String accessType);
}
