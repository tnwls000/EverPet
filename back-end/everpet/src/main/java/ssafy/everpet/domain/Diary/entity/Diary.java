package ssafy.everpet.domain.Diary.entity;

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
public class Diary {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private String imageUrl;

    @Column(columnDefinition = "TEXT")
    private String content;

    private LocalDateTime createTime;

    private LocalDateTime updateTime;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    //==연관관계 메서드==//
    public void setUser(User user) {
        this.user = user;
        user.getDiaries().add(this);
    }

    //==비즈니스 로직==//
    public void updateContent(String content) {
        this.content = content;
    }
}
