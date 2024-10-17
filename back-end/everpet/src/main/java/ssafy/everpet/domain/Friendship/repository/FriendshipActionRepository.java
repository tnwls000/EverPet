package ssafy.everpet.domain.Friendship.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ssafy.everpet.domain.Friendship.entity.FriendshipAction;

@Repository
public interface FriendshipActionRepository extends JpaRepository<FriendshipAction, Integer> {
}
