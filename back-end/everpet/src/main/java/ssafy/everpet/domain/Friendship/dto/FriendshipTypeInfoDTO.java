package ssafy.everpet.domain.Friendship.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class FriendshipTypeInfoDTO {
    private int id;
    private String style;
    private int initFriendship;
    private int styleCondition;
}
