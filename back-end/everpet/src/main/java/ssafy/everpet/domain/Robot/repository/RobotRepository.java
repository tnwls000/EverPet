package ssafy.everpet.domain.Robot.repository;

import io.lettuce.core.dynamic.annotation.Param;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import ssafy.everpet.domain.Robot.entity.Robot;
import org.springframework.data.jpa.repository.JpaRepository;
import ssafy.everpet.domain.User.entity.User;

import java.util.Optional;

@Repository
public interface RobotRepository extends JpaRepository<Robot, Integer> {
    Optional<Robot> findByUser(User user);
}
