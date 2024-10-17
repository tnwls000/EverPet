package ssafy.everpet.domain.AccessLog.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ssafy.everpet.domain.AccessLog.entity.AccessLog;
import ssafy.everpet.domain.User.entity.User;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface AccessLogRepository extends JpaRepository<AccessLog, Integer> {
    List<AccessLog> findAllByUserAndAccessTypeAndAccessTimeBetweenOrderByAccessTimeDesc(User user, String accessType, LocalDateTime start, LocalDateTime end);
    List<AccessLog> findAllByUserAndAccessTypeOrderByAccessTimeDesc(User user, String accessType);
    List<AccessLog> findAllByUserAndAccessTimeBetweenOrderByAccessTimeDesc(User user, LocalDateTime start, LocalDateTime end);
    List<AccessLog> findAllByUserOrderByAccessTimeDesc(User user);
}
