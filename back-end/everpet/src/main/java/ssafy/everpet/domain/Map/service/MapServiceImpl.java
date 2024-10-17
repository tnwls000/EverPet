package ssafy.everpet.domain.Map.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ssafy.everpet.domain.Map.dto.MapInfoDTO;
import ssafy.everpet.domain.Map.dto.MapSaveDTO;
import ssafy.everpet.domain.Map.entity.Map;
import ssafy.everpet.domain.Map.repository.MapRepository;
import ssafy.everpet.domain.Robot.entity.Robot;
import ssafy.everpet.domain.Robot.entity.SerialNumber;
import ssafy.everpet.domain.Robot.repository.RobotRepository;
import ssafy.everpet.domain.Robot.repository.SerialNumberRepository;
import ssafy.everpet.domain.User.entity.User;
import ssafy.everpet.domain.User.repository.UserRepository;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class MapServiceImpl implements MapService {

    private final UserRepository userRepository;
    private final RobotRepository robotRepository;
    private final MapRepository mapRepository;
    private final SerialNumberRepository serialNumberRepository;

    @Override
    @Transactional
    public void saveOrUpdateMap(MapSaveDTO mapSaveDTO) {
        User user = userRepository.findByUserId(mapSaveDTO.getUserId()).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));

        List<Short> shortList = new ArrayList<>();
        for (short s : mapSaveDTO.getData()) {
            shortList.add(s);
        }

        Optional<Map> mapOptional = mapRepository.findByUser(user);
        if (mapOptional.isPresent()) { // 이미 지도 데이터 있는 경우 수정
            Map map = mapOptional.get();
            map.updateMap(mapSaveDTO, shortList);
            map.setUser(user);
        } else { // 지도 데이터 없는 경우 새로 저장
            Map map = Map.builder()
                    .user(user)
                    .data(shortList)
                    .height(mapSaveDTO.getHeight())
                    .width(mapSaveDTO.getWidth())
                    .resolution(mapSaveDTO.getResolution())
                    .orientationX(mapSaveDTO.getOrientationX())
                    .orientationY(mapSaveDTO.getOrientationY())
                    .orientationZ(mapSaveDTO.getOrientationZ())
                    .orientationW(mapSaveDTO.getOrientationW())
                    .positionX(mapSaveDTO.getPositionX())
                    .positionY(mapSaveDTO.getPositionY())
                    .positionZ(mapSaveDTO.getPositionZ())
                    .build();
            map.setUser(user);
            mapRepository.save(map);
        }
    }

    @Override
    public MapInfoDTO getMapInfo(int id) {
        User user = userRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        Map map = mapRepository.findByUser(user).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_MAP));

        Robot robot = robotRepository.findByUser(user).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_ROBOT));
        SerialNumber serialNumber = serialNumberRepository.findByRobot(robot).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_SERIAL_NUMBER));

        short[] shorts = new short[map.getData().size()];

        // List의 각 요소를 배열에 복사
        for (int i = 0; i < map.getData().size(); i++) {
            shorts[i] = map.getData().get(i);
        }

        return MapInfoDTO.builder()
                .width(map.getWidth())
                .height(map.getHeight())
                .resolution(map.getResolution())
                .data(shorts)
                .positionX(map.getPositionX())
                .positionY(map.getPositionY())
                .positionZ(map.getPositionZ())
                .orientationX(map.getOrientationX())
                .orientationY(map.getOrientationY())
                .orientationZ(map.getOrientationZ())
                .orientationW(map.getOrientationW())
                .serialNumber(serialNumber.getSerialNumber())
                .build();
    }
}
