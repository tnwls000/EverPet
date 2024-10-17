package ssafy.everpet.domain.AccessLog.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ssafy.everpet.domain.AccessLog.dto.AccessLogInfoDTO;
import ssafy.everpet.domain.AccessLog.entity.AccessLog;
import ssafy.everpet.domain.AccessLog.repository.AccessLogRepository;
import ssafy.everpet.domain.User.entity.User;
import ssafy.everpet.domain.User.repository.UserRepository;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class AccessLogServiceImpl implements AccessLogService{

    private final UserRepository userRepository;
    private final AccessLogRepository accessLogRepository;

    @Override
    public List<AccessLogInfoDTO> getAccessLogs(String userId, String accessType, LocalDateTime start, LocalDateTime end) {
        User user = userRepository.findByUserId(userId).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));

        if (accessType != null && start != null && end != null) {
            return convertToDTOs(accessLogRepository.findAllByUserAndAccessTypeAndAccessTimeBetweenOrderByAccessTimeDesc(user, accessType, start, end));
        } else if (accessType != null) {
            return convertToDTOs(accessLogRepository.findAllByUserAndAccessTypeOrderByAccessTimeDesc(user, accessType));
        } else if (start != null && end != null) {
            return convertToDTOs(accessLogRepository.findAllByUserAndAccessTimeBetweenOrderByAccessTimeDesc(user, start, end));
        } else {
            return convertToDTOs(accessLogRepository.findAllByUserOrderByAccessTimeDesc(user));
        }
    }

    @Override
    @Transactional
    public void saveAccessLog(String userId, LocalDateTime accessTime, String accessType) {
        User user = userRepository.findByUserId(userId).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        AccessLog accessLog = AccessLog.builder()
                .accessTime(accessTime)
                .accessType(accessType)
                .user(user)
                .build();
        accessLog.setUser(user);
        accessLogRepository.save(accessLog);
    }

    private List<AccessLogInfoDTO> convertToDTOs(List<AccessLog> accessLogs) {
        return accessLogs.stream()
                .map(this::convertToDTO)
                .toList();
    }

    private AccessLogInfoDTO convertToDTO(AccessLog accessLog) {
        return AccessLogInfoDTO.builder()
                .accessId(accessLog.getId())
                .accessTime(accessLog.getAccessTime())
                .accessType(accessLog.getAccessType())
                .build();
    }
}
