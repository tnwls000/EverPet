package ssafy.everpet.domain.Robot.service;

import ssafy.everpet.domain.Robot.dto.RobotInfoDTO;
import ssafy.everpet.domain.Robot.dto.RobotSaveDTO;
import ssafy.everpet.domain.Robot.dto.RobotUpdateDTO;
import ssafy.everpet.domain.Robot.dto.UserRobotDTO;

public interface RobotService {
    UserRobotDTO saveRobot(RobotSaveDTO robotSaveDTO);

    void verifySerialNumber(String serialNumber);

    RobotInfoDTO getRobotInfoByUserId(int id);

    void modifyRobot(int id, RobotUpdateDTO robotUpdateDTO);

    void updateCurrentFriendship(String userId, double friendship);
}
