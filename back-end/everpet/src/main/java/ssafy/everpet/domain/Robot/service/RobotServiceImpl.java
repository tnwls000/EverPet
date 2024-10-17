package ssafy.everpet.domain.Robot.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ssafy.everpet.domain.Friendship.entity.FriendshipType;
import ssafy.everpet.domain.Friendship.repository.FriendshipTypeRepository;
import ssafy.everpet.domain.Robot.dto.RobotInfoDTO;
import ssafy.everpet.domain.Robot.dto.RobotSaveDTO;
import ssafy.everpet.domain.Robot.dto.RobotUpdateDTO;
import ssafy.everpet.domain.Robot.dto.UserRobotDTO;
import ssafy.everpet.domain.Robot.entity.Robot;
import ssafy.everpet.domain.Robot.repository.RobotRepository;
import ssafy.everpet.domain.Robot.entity.SerialNumber;
import ssafy.everpet.domain.Robot.repository.SerialNumberRepository;
import ssafy.everpet.domain.User.entity.User;
import ssafy.everpet.domain.User.repository.UserRepository;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class RobotServiceImpl implements RobotService{

    private final RobotRepository robotRepository;
    private final UserRepository userRepository;
    private final SerialNumberRepository serialNumberRepository;
    private final FriendshipTypeRepository friendshipTypeRepository;

    @Override
    public UserRobotDTO saveRobot(RobotSaveDTO robotSaveDTO) {
        User user = userRepository.findByUserId(robotSaveDTO.getUserId())
                .orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));

        FriendshipType friendshipType = friendshipTypeRepository.findByStyle(robotSaveDTO.getRobotStyle()).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_FRIENDSHIP_TYPE));

        Robot robot = Robot.builder()
                .user(user)
                .name(robotSaveDTO.getRobotName())
                .style(robotSaveDTO.getRobotStyle())
                .gender(robotSaveDTO.getRobotGender())
                .currentFriendship(friendshipType.getInitFriendship())
                .createTime(LocalDateTime.now())
                .updateTime(LocalDateTime.now())
                .build();
        robot.setUser(user);

        SerialNumber serialNumber = serialNumberRepository.findBySerialNumber(robotSaveDTO.getRobotSerialNumber())
                .orElseThrow(() -> new CustomException(ErrorCode.INVALID_SERIAL_NUMBER_ID));
        serialNumber.setRobot(robot);

        Robot savedRobot = robotRepository.save(robot);

        return converToUserRobotDTO(user, savedRobot, serialNumber);
    }

    private UserRobotDTO converToUserRobotDTO(User user, Robot robot, SerialNumber serialNumber) {
        return UserRobotDTO.builder()
                .userID(user.getUserId())
                .userName(user.getName())
                .userGender(user.getGender())
                .userAge(user.getAge())
                .robotName(robot.getName())
                .robotStyle(robot.getStyle())
                .robotGender(robot.getGender())
                .currentFriendship(robot.getCurrentFriendship())
                .serialNumber(serialNumber.getSerialNumber())
                .build();
    }

    @Override
    public void verifySerialNumber(String serialNumber) {
        SerialNumber foundserialNumber = serialNumberRepository.findBySerialNumber(serialNumber).orElseThrow(() -> new CustomException(ErrorCode.INVALID_SERIAL_NUMBER_ID));
        if (foundserialNumber.getRobot() != null) throw new CustomException(ErrorCode.DUPLICATE_SERIAL_NUMBER);

    }

    @Override
    public RobotInfoDTO getRobotInfoByUserId(int id) {
        User user = userRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        Robot robot = robotRepository.findByUser(user)
                .orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_ROBOT));
        SerialNumber serialNumber = serialNumberRepository.findByRobot(robot)
                .orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_SERIAL_NUMBER));

        return converToRobotInfoDTO(robot, serialNumber.getSerialNumber());
    }

    @Override
    @Transactional
    public void modifyRobot(int id, RobotUpdateDTO robotUpdateDTO) {
        User user = userRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        Robot robot = robotRepository.findByUser(user)
                .orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_ROBOT));
        robot.updateRobot(robotUpdateDTO);
    }

    @Override
    @Transactional
    public void updateCurrentFriendship(String userId, double friendship) {
        User user = userRepository.findByUserId(userId).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        Robot robot = robotRepository.findByUser(user)
                .orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_ROBOT));
        robot.updateCurrentFriendship(friendship);
    }

    private RobotInfoDTO converToRobotInfoDTO(Robot robot, String serialNumber) {
        return RobotInfoDTO.builder()
                .robotSerialNumber(serialNumber)
                .robotName(robot.getName())
                .robotStyle(robot.getStyle())
                .robotGender(robot.getGender())
                .build();
    }
}
