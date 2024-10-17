package ssafy.everpet.domain.User.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ssafy.everpet.domain.Robot.dto.UserRobotDTO;
import ssafy.everpet.domain.Robot.entity.Robot;
import ssafy.everpet.domain.Robot.entity.SerialNumber;
import ssafy.everpet.domain.Robot.repository.RobotRepository;
import ssafy.everpet.domain.Robot.repository.SerialNumberRepository;
import ssafy.everpet.domain.User.dto.*;
import ssafy.everpet.domain.User.entity.User;
import ssafy.everpet.domain.User.entity.UserRole;
import ssafy.everpet.domain.User.repository.UserRepository;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;
import ssafy.everpet.global.util.JwtTokenUtil;

import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final RobotRepository robotRepository;
    private final SerialNumberRepository serialNumberRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenUtil jwtTokenUtil;

    @Override
    public void signUp(UserSignUpDTO userSignUpDTO) {
        User user = User.builder()
                .userId(userSignUpDTO.getUserId())
                .password(passwordEncoder.encode(userSignUpDTO.getPassword()))
                .name(userSignUpDTO.getName())
                .email(userSignUpDTO.getEmail())
                .phoneNumber(userSignUpDTO.getPhoneNumber())
                .gender(userSignUpDTO.getGender())
                .age(userSignUpDTO.getAge())
                .userRole(UserRole.USER)
                .build();

        userRepository.save(user);
    }

    @Override
    public int login(UserLoginDTO userLoginDTO) {
        User user = userRepository.findByUserId(userLoginDTO.getUserId()).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        if (!user.getUserId().equals(userLoginDTO.getUserId()) || !passwordEncoder.matches(userLoginDTO.getPassword(), user.getPassword())) {
            throw new CustomException(ErrorCode.INCORRECT_ID_OR_PASSWORD);
        }
        return user.getId();
    }

    @Override
    public void validateUserId(String userId) {
        Optional<User> userOptional = userRepository.findByUserId(userId);
        if (userOptional.isPresent()) throw new CustomException(ErrorCode.DUPLICATE_USER_ID);
    }

    @Override
    public UserInfoDTO getUserInfo(int id) {
        User user = userRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        return convertToDTO(user);
    }

    @Override
    public User getUserInfoByUserId(String userId) {
        return userRepository.findByUserId(userId).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
    }

    @Override
    @Transactional
    public void modifyUser(int id, UserUpdateDTO userUpdateDTO) {
        User user = userRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        if (!passwordEncoder.matches(userUpdateDTO.getPassword(), user.getPassword())) throw new CustomException(ErrorCode.INCORRECT_PASSWORD);

        String password = userUpdateDTO.getNewPassword() == null ? user.getPassword() : passwordEncoder.encode(userUpdateDTO.getNewPassword());
        user.updateUser(userUpdateDTO, password);
    }

    @Override
    public void deleteUser(int id, String password) {
        User user = userRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));

        if (!passwordEncoder.matches(password, user.getPassword())) throw new CustomException(ErrorCode.INCORRECT_PASSWORD);

        Robot robot = robotRepository.findByUser(user).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_ROBOT));
        SerialNumber serialNumber = serialNumberRepository.findByRobot(robot).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_SERIAL_NUMBER));
        SerialNumber newSerialNumber = SerialNumber.builder().serialNumber(serialNumber.getSerialNumber()).build();

        userRepository.delete(user);
        serialNumberRepository.save(newSerialNumber); // 시리얼 넘버는 삭제되지 않아야 함
    }

    @Override
    public void logout(int id, String accessToken) {
        User user = userRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        jwtTokenUtil.setBlackList(accessToken, "blacklisted");
        if (jwtTokenUtil.getRefreshToken(id).isPresent()) jwtTokenUtil.deleteRefreshToken(id);
        else throw new CustomException(ErrorCode.JWT_BLACKLISTED);
    }

    @Override
    public String findId(UserFindIdDTO userFindIdDTO) {
        User user = userRepository.findByNameAndEmail(userFindIdDTO.getName(), userFindIdDTO.getEmail()).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_NAME_AND_EMAIL));
        return user.getUserId();
    }

    @Override
    public User findPassword(UserFindPasswordDTO userFindPasswordDTO) {
        return userRepository.findByUserIdAndEmail(userFindPasswordDTO.getUserId(), userFindPasswordDTO.getEmail()).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_USERID_AND_EMAIL));
    }

    @Override
    public UserRobotDTO getUserRobotInfo(int id) {
        User user = userRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        Robot robot = robotRepository.findByUser(user).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_ROBOT));
        SerialNumber serialNumber = serialNumberRepository.findByRobot(robot).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_SERIAL_NUMBER));

        return convertToUserRobotDTO(user, robot, serialNumber);
    }

    @Override
    public void checkEmailDuplication(String email) {
        Optional<User> foundUser = userRepository.findByEmail(email);
        if (foundUser.isPresent()) throw new CustomException(ErrorCode.DUPLICATE_EMAIL);
    }

    private UserRobotDTO convertToUserRobotDTO(User user, Robot robot, SerialNumber serialNumber) {
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

    private UserInfoDTO convertToDTO(User user) {
        return UserInfoDTO.builder()
                .userId(user.getUserId())
                .name(user.getName())
                .email(user.getEmail())
                .phoneNumber(user.getPhoneNumber())
                .gender(user.getGender())
                .age(user.getAge())
                .build();
    }
}
