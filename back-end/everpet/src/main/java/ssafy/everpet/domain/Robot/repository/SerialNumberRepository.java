package ssafy.everpet.domain.Robot.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ssafy.everpet.domain.Robot.entity.Robot;
import ssafy.everpet.domain.Robot.entity.SerialNumber;

import java.util.Optional;

@Repository
public interface SerialNumberRepository extends JpaRepository<SerialNumber, String> {

    Optional<SerialNumber> findBySerialNumber(String seiralNumber);

    Optional<SerialNumber> findByRobot(Robot robot);
}
