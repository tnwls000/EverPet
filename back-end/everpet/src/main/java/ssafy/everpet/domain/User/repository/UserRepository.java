package ssafy.everpet.domain.User.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ssafy.everpet.domain.User.entity.User;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {

    Optional<User> findByUserId(String userId);

    Optional<User> findByNameAndEmail(String name, String email);

    Optional<User> findByUserIdAndEmail(String userId, String email);

    Optional<User> findByEmail(String email);
}
