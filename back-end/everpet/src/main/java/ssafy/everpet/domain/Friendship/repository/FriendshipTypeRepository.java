package ssafy.everpet.domain.Friendship.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ssafy.everpet.domain.Friendship.entity.FriendshipType;

import java.util.Optional;

@Repository
public interface FriendshipTypeRepository extends JpaRepository<FriendshipType, Integer> {
    Optional<FriendshipType> findByStyle(String style);
}
