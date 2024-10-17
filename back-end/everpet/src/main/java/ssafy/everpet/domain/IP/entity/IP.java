package ssafy.everpet.domain.IP.entity;

import ssafy.everpet.domain.Robot.entity.SerialNumber;
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
public class IP {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "serial_number_id")
    private SerialNumber serialNumber;

    @Column(length = 100)
    private String ipAddress;

    // ==연관관계 메서드== //
    public void setSerialNumber(SerialNumber serialNumber) {
        this.serialNumber = serialNumber;
        serialNumber.setIp(this);
    }
}
