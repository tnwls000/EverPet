package ssafy.everpet.domain.User.service;

import ssafy.everpet.domain.Robot.dto.UserRobotDTO;
import ssafy.everpet.domain.User.dto.*;
import ssafy.everpet.domain.User.entity.User;

public interface UserService {
    void signUp(UserSignUpDTO userSignUpDTO);

    int login(UserLoginDTO userLoginDTO);

    void validateUserId(String userId);

    UserInfoDTO getUserInfo(int id);

    User getUserInfoByUserId(String userId);

    void modifyUser(int id, UserUpdateDTO userUpdateDTO);

    void deleteUser(int id, String password);

    void logout(int id, String accessToken);

    String findId(UserFindIdDTO userFindIdDTO);

    User findPassword(UserFindPasswordDTO userFindPasswordDTO);

    UserRobotDTO getUserRobotInfo(int id);

    void checkEmailDuplication(String email);
}
