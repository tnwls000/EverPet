package ssafy.everpet.domain.Friendship.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class FriendshipActionUpdateDTO {
    private String actionType;
    private double low;
    private double medium;
    private double high;
}
