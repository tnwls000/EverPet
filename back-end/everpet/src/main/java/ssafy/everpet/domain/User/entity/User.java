package ssafy.everpet.domain.User.entity;

import ssafy.everpet.domain.AccessLog.entity.AccessLog;
import ssafy.everpet.domain.Diary.entity.Diary;
import ssafy.everpet.domain.Map.entity.Map;
import ssafy.everpet.domain.Robot.entity.Robot;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import ssafy.everpet.domain.User.dto.UserUpdateDTO;

import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
@Table(name = "Users")
public class User {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(length = 20)
    private String userId;

    @Column(length = 20)
    private String name;

    @Column(length = 50)
    private String email;

    private String password;

    @Column(length = 20)
    private String phoneNumber;

    @Column(length = 10)
    private String gender;

    private int age;

    @Enumerated(EnumType.STRING)
    private UserRole userRole;

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private Robot robot;

    @Builder.Default
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<AccessLog> accessLogs = new ArrayList<>();

    @Builder.Default
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Diary> diaries = new ArrayList<>();

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private Map map;

    // == 연관관계 메서드 == //
    public void setRobot(Robot robot) {
        this.robot = robot;
    }

    public void setMap(Map map) {
        this.map = map;
    }

    // == 비즈니스 로직 == //
    public void updateUser(UserUpdateDTO userUpdateDTO, String newPassword) {
        this.name = userUpdateDTO.getName();
        this.email = userUpdateDTO.getEmail();
        this.password = newPassword;
        this.phoneNumber = userUpdateDTO.getPhoneNumber();
        this.gender = userUpdateDTO.getGender();
        this.age = userUpdateDTO.getAge();
    }

    public void updatePassword(String newPassword) {
        this.password = newPassword;
    }
}
