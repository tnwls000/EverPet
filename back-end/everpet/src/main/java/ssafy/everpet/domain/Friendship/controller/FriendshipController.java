package ssafy.everpet.domain.Friendship.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import ssafy.everpet.domain.Friendship.dto.FriendshipActionUpdateDTO;
import ssafy.everpet.domain.Friendship.dto.FriendshipInfoDTO;
import ssafy.everpet.domain.Friendship.dto.FriendshipTypeUpdateDTO;
import ssafy.everpet.domain.Friendship.service.FriendshipService;
import ssafy.everpet.domain.User.entity.CustomUserDetails;

@RestController
@RequestMapping("/admin/friendship")
@RequiredArgsConstructor
public class FriendshipController {

    private final FriendshipService friendshipService;

    @GetMapping
    public ResponseEntity<FriendshipInfoDTO> getFriendshipInfo(@AuthenticationPrincipal CustomUserDetails customUserDetails) {
        FriendshipInfoDTO friendshipInfo = friendshipService.getFriendshipInfo();
        return new ResponseEntity<>(friendshipInfo, HttpStatus.OK);
    }

    @PatchMapping("/type/{typeId}")
    public ResponseEntity<String> modifyFriendshipType(@AuthenticationPrincipal CustomUserDetails customUserDetails,
                                                       @RequestBody FriendshipTypeUpdateDTO friendshipTypeUpdateDTO,
                                                       @PathVariable("typeId") int typeId) {
        friendshipService.modifyFriendshipType(typeId, friendshipTypeUpdateDTO);
        return ResponseEntity.status(HttpStatus.OK).body("친밀도 타입 수정 성공");
    }

    @PatchMapping("/action/{actionId}")
    public ResponseEntity<String> modifyFriendshipAction(@AuthenticationPrincipal CustomUserDetails customUserDetails,
                                                       @RequestBody FriendshipActionUpdateDTO friendshipActionUpdateDTO,
                                                       @PathVariable("actionId") int actionId) {
        friendshipService.modifyFriendshipAction(actionId, friendshipActionUpdateDTO);
        return ResponseEntity.status(HttpStatus.OK).body("친밀도 행동 수정 성공");
    }
}
