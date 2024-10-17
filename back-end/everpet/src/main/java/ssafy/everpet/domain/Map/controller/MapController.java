package ssafy.everpet.domain.Map.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import ssafy.everpet.domain.Map.dto.MapInfoDTO;
import ssafy.everpet.domain.Map.service.MapService;
import ssafy.everpet.domain.Robot.dto.RobotInfoDTO;
import ssafy.everpet.domain.Robot.service.RobotService;
import ssafy.everpet.domain.User.entity.CustomUserDetails;
import ssafy.everpet.global.exception.CustomException;

@RequestMapping("/map")
@RestController
@RequiredArgsConstructor
public class MapController {

    private final MapService mapService;
    private final RobotService robotService;

    @GetMapping
    public ResponseEntity<?> getMap(@AuthenticationPrincipal CustomUserDetails customUserDetails) {
        int id = customUserDetails.getId();
        try {
            MapInfoDTO mapInfo = mapService.getMapInfo(id);
            return ResponseEntity.ok(mapInfo);
        } catch (CustomException e) {
            RobotInfoDTO robotInfoDTO = robotService.getRobotInfoByUserId(id);
            String serialNumber = robotInfoDTO.getRobotSerialNumber();
            return ResponseEntity.ok(serialNumber);
        }
    }
}
