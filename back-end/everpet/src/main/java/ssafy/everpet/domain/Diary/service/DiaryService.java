package ssafy.everpet.domain.Diary.service;

import ssafy.everpet.domain.Diary.dto.DiaryInfoDTO;
import ssafy.everpet.domain.Diary.dto.DiarySaveDTO;
import ssafy.everpet.domain.Diary.dto.DiaryUpdateDTO;

import java.util.List;

public interface DiaryService {
    void saveDiary(String userId, DiarySaveDTO diarySaveDTO);
    List<DiaryInfoDTO> getDiaries(int userId);
    DiaryInfoDTO getDiary(int userId, int diaryId);
    void modifyDiary(int userId, int diaryId, DiaryUpdateDTO diaryUpdateDTO);
    void deleteDiary(int userId, int diaryId);
}
