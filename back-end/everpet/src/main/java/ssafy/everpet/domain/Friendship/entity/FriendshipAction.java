package ssafy.everpet.domain.Friendship.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import ssafy.everpet.domain.Friendship.dto.FriendshipActionUpdateDTO;

@Entity
@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class FriendshipAction {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(length = 20)
    private String actionType;

    private double low;

    private double medium;

    private double high;

    //==비즈니스 로직==//
    public void updateFriendshipAction(FriendshipActionUpdateDTO friendshipActionUpdateDTO) {
        this.actionType = friendshipActionUpdateDTO.getActionType();
        this.low = friendshipActionUpdateDTO.getLow();
        this.medium = friendshipActionUpdateDTO.getMedium();
        this.high = friendshipActionUpdateDTO.getHigh();
    }
}
