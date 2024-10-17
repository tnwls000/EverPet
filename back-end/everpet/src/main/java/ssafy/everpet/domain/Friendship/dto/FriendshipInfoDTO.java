package ssafy.everpet.domain.Friendship.dto;

import lombok.Builder;
import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

@Getter
@Builder
public class FriendshipInfoDTO {

    @Builder.Default
    List<FriendshipTypeInfoDTO> friendshipTypeInfoList = new ArrayList<>();

    @Builder.Default
    List<FriendshipActionInfoDTO> friendshipActionInfoList = new ArrayList<>();

}
