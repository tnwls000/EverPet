package ssafy.everpet.domain.Diary.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ssafy.everpet.domain.Diary.dto.DiaryInfoDTO;
import ssafy.everpet.domain.Diary.dto.DiarySaveDTO;
import ssafy.everpet.domain.Diary.dto.DiaryUpdateDTO;
import ssafy.everpet.domain.Diary.entity.Diary;
import ssafy.everpet.domain.Diary.repository.DiaryRepository;
import ssafy.everpet.domain.User.entity.User;
import ssafy.everpet.domain.User.repository.UserRepository;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class DiaryServiceImpl implements DiaryService {

    private final UserRepository userRepository;
    private final DiaryRepository diaryRepository;

    @Override
    public void saveDiary(String userId, DiarySaveDTO diarySaveDTO) {
        User user = userRepository.findByUserId(userId).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));

        Diary diary = Diary.builder()
                .user(user)
                .content(diarySaveDTO.getContent())
                .imageUrl(diarySaveDTO.getImageUrl())
                .createTime(LocalDateTime.now())
                .updateTime(LocalDateTime.now())
                .build();
        diary.setUser(user);

        diaryRepository.save(diary);
    }

    @Override
    public List<DiaryInfoDTO> getDiaries(int userId) {
        User user = userRepository.findById(userId).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        List<Diary> diaries = diaryRepository.findAllByUserOrderByCreateTimeDesc(user);
        return convertToDTOs(diaries);
    }

    @Override
    public DiaryInfoDTO getDiary(int userId, int diaryId) {
        Diary diary = validateDiary(userId, diaryId);
        return convertToDTO(diary);
    }

    @Override
    @Transactional
    public void modifyDiary(int userId, int diaryId, DiaryUpdateDTO diaryUpdateDTO) {
        Diary diary = validateDiary(userId, diaryId);
        diary.updateContent(diaryUpdateDTO.getContent());
    }

    @Override
    public void deleteDiary(int userId, int diaryId) {
        Diary diary = validateDiary(userId, diaryId);
        diaryRepository.delete(diary);
    }

    private Diary validateDiary(int userId, int diaryId) {
        User user = userRepository.findById(userId).orElseThrow(() -> new CustomException(ErrorCode.INVALID_USER_ID));
        Diary diary = diaryRepository.findById(diaryId).orElseThrow(() -> new CustomException(ErrorCode.INVALID_DIARY_ID));
        if (user.getId() != diary.getUser().getId()) throw new CustomException(ErrorCode.NOT_MATCH_DIARY_AND_USER);
        return diary;
    }

    private List<DiaryInfoDTO> convertToDTOs(List<Diary> diaries) {
        return diaries.stream()
                .map(this::convertToDTO)
                .toList();
    }

    private DiaryInfoDTO convertToDTO(Diary diary) {
        return DiaryInfoDTO.builder()
                .diaryId(diary.getId())
                .diaryContent(diary.getContent())
                .imageUrl(diary.getImageUrl())
                .createTime(diary.getCreateTime())
                .build();
    }
}
