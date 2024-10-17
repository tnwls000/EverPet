package ssafy.everpet.domain.AccessLog.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import ssafy.everpet.domain.User.entity.User;

import java.time.LocalDateTime;

@Entity
@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class AccessLog {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private LocalDateTime accessTime;

    @Column(length = 20)
    private String accessType;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    //==연관관계 메서드==//
    public void setUser(User user) {
        this.user = user;
        user.getAccessLogs().add(this);
    }

}
