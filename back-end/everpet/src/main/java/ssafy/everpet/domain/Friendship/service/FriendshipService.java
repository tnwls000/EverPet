package ssafy.everpet.domain.Friendship.service;

import ssafy.everpet.domain.Friendship.dto.FriendshipActionUpdateDTO;
import ssafy.everpet.domain.Friendship.dto.FriendshipInfoDTO;
import ssafy.everpet.domain.Friendship.dto.FriendshipTypeUpdateDTO;

public interface FriendshipService {
    FriendshipInfoDTO getFriendshipInfo();
    void modifyFriendshipType(int id, FriendshipTypeUpdateDTO friendshipTypeUpdateDTO);
    void modifyFriendshipAction(int id, FriendshipActionUpdateDTO friendshipActionUpdateDTO);
    int findInitFriendshipByTypeStyle(String style);
}
