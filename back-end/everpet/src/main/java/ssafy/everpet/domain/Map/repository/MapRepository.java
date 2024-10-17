package ssafy.everpet.domain.Map.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ssafy.everpet.domain.Map.entity.Map;
import ssafy.everpet.domain.User.entity.User;

import java.util.Optional;

@Repository
public interface MapRepository extends JpaRepository<Map, Integer> {
    Optional<Map> findByUser(User user);
}
