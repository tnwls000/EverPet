package ssafy.everpet.domain.Friendship.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class FriendshipTypeUpdateDTO {
    private String style;
    private int initFriendship;
    private int styleCondition;
}
