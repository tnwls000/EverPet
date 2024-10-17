package ssafy.everpet.domain.Diary.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ssafy.everpet.domain.Diary.entity.Diary;
import ssafy.everpet.domain.User.entity.User;

import java.util.List;

@Repository
public interface DiaryRepository extends JpaRepository<Diary, Integer> {
    List<Diary> findAllByUserOrderByCreateTimeDesc(User user);
}
