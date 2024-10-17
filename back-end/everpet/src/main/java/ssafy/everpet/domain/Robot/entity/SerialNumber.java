package ssafy.everpet.domain.Robot.entity;

import ssafy.everpet.domain.IP.entity.IP;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Entity
@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class SerialNumber {

    @Id
    @Column(length = 100)
    private String serialNumber;

    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "robot_id")
    private Robot robot;

    @OneToOne(mappedBy = "serialNumber", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private IP ip;

    // ==연관관계 메서드== //
    public void setRobot(Robot robot) {
        this.robot = robot;
        robot.setSerialNumber(this);
    }

    public void setIp(IP ip) {
        this.ip = ip;
    }
}
