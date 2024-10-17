package ssafy.everpet.domain.Friendship.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ssafy.everpet.domain.Friendship.dto.*;
import ssafy.everpet.domain.Friendship.entity.FriendshipAction;
import ssafy.everpet.domain.Friendship.entity.FriendshipType;
import ssafy.everpet.domain.Friendship.repository.FriendshipActionRepository;
import ssafy.everpet.domain.Friendship.repository.FriendshipTypeRepository;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;

import java.util.List;

@Service
@RequiredArgsConstructor
public class FriendshipServiceImpl implements FriendshipService {

    private final FriendshipTypeRepository friendshipTypeRepository;
    private final FriendshipActionRepository friendshipActionRepository;

    @Override
    public FriendshipInfoDTO getFriendshipInfo() {
        List<FriendshipType> friendshipTypes = friendshipTypeRepository.findAll();
        List<FriendshipAction> friendshipActions = friendshipActionRepository.findAll();

        FriendshipInfoDTO friendshipInfoDTO = FriendshipInfoDTO.builder().build();
        for (FriendshipType friendshipType : friendshipTypes) {
            friendshipInfoDTO.getFriendshipTypeInfoList().add(convertToTypeDTO(friendshipType));
        }
        for (FriendshipAction friendshipAction : friendshipActions) {
            friendshipInfoDTO.getFriendshipActionInfoList().add(convertToActionDTO(friendshipAction));
        }
        return friendshipInfoDTO;
    }

    @Override
    @Transactional
    public void modifyFriendshipType(int id, FriendshipTypeUpdateDTO friendshipTypeUpdateDTO) {
        FriendshipType friendshipType = friendshipTypeRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_FRIENDSHIP_TYPE_ID));
        friendshipType.updateFriendshipType(friendshipTypeUpdateDTO);
    }

    @Override
    @Transactional
    public void modifyFriendshipAction(int id, FriendshipActionUpdateDTO friendshipActionUpdateDTO) {
        FriendshipAction friendshipAction = friendshipActionRepository.findById(id).orElseThrow(() -> new CustomException(ErrorCode.INVALID_FRIENDSHIP_ACTION_ID));
        friendshipAction.updateFriendshipAction(friendshipActionUpdateDTO);
    }

    @Override
    public int findInitFriendshipByTypeStyle(String style) {
        FriendshipType friendshipType = friendshipTypeRepository.findByStyle(style).orElseThrow(() -> new CustomException(ErrorCode.NOT_FOUND_FRIENDSHIP_TYPE));
        return friendshipType.getInitFriendship();
    }

    private FriendshipTypeInfoDTO convertToTypeDTO(FriendshipType friendshipType) {
        return FriendshipTypeInfoDTO.builder()
                .id(friendshipType.getId())
                .style(friendshipType.getStyle())
                .initFriendship(friendshipType.getInitFriendship())
                .styleCondition(friendshipType.getStyleCondition())
                .build();
    }

    private FriendshipActionInfoDTO convertToActionDTO(FriendshipAction friendshipAction) {
        return FriendshipActionInfoDTO.builder()
                .id(friendshipAction.getId())
                .actionType(friendshipAction.getActionType())
                .low(friendshipAction.getLow())
                .medium(friendshipAction.getMedium())
                .high(friendshipAction.getHigh())
                .build();
    }
}
