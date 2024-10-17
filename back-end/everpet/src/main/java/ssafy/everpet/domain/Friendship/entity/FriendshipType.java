package ssafy.everpet.domain.Friendship.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import ssafy.everpet.domain.Friendship.dto.FriendshipTypeUpdateDTO;

@Entity
@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class FriendshipType {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(length = 20)
    private String style;

    private int initFriendship;

    private int styleCondition;

    //==비즈니스 로직==//
    public void updateFriendshipType(FriendshipTypeUpdateDTO friendshipTypeUpdateDTO) {
        this.style = friendshipTypeUpdateDTO.getStyle();
        this.initFriendship = friendshipTypeUpdateDTO.getInitFriendship();
        this.styleCondition = friendshipTypeUpdateDTO.getStyleCondition();
    }
}
