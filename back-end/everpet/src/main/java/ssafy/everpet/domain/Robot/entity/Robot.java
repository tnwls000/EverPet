package ssafy.everpet.domain.Robot.entity;

import ssafy.everpet.domain.Robot.dto.RobotUpdateDTO;
import ssafy.everpet.domain.User.entity.User;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Robot {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    @OneToOne(mappedBy = "robot", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private SerialNumber serialNumber;

    @Column(length = 20)
    private String name;

    @Column(length = 20)
    private String style;

    @Column(length = 10)
    private String gender;

    private double currentFriendship;

    private LocalDateTime createTime;

    private LocalDateTime updateTime;

    // ==연관관계 메서드== //
    public void setUser(User user) {
        this.user = user;
        user.setRobot(this);
    }

    public void setSerialNumber(SerialNumber serialNumber) {
        this.serialNumber = serialNumber;
    }

    // ==비즈니스 로직== //
    public void updateRobot(RobotUpdateDTO robotUpdateDTO) {
        this.name = robotUpdateDTO.getRobotName();
        this.style = robotUpdateDTO.getRobotStyle();
        this.gender = robotUpdateDTO.getRobotGender();
        this.updateTime = LocalDateTime.now();
    }

    public void updateCurrentFriendship(double currentFriendship) {
        this.currentFriendship = currentFriendship;
    }
}
