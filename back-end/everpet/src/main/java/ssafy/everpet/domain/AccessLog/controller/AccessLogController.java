package ssafy.everpet.domain.AccessLog.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import ssafy.everpet.domain.AccessLog.dto.AccessLogInfoDTO;
import ssafy.everpet.domain.AccessLog.service.AccessLogService;
import ssafy.everpet.domain.User.entity.CustomUserDetails;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/access")
@RequiredArgsConstructor
public class AccessLogController {

    private final AccessLogService accessLogService;

    @GetMapping
    public ResponseEntity<List<AccessLogInfoDTO>> getAccessLogs(
            @AuthenticationPrincipal CustomUserDetails customUserDetails,
            @RequestParam(required = false) String accessType,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime startDate,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endDate
    ) {
        String userId = customUserDetails.getUserId();
        List<AccessLogInfoDTO> accessLogs = accessLogService.getAccessLogs(userId, accessType, startDate, endDate);
        return ResponseEntity.ok(accessLogs);
    }
}
