package ssafy.everpet.domain.Friendship.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class FriendshipActionInfoDTO {
    private int id;
    private String actionType;
    private double low;
    private double medium;
    private double high;
}
