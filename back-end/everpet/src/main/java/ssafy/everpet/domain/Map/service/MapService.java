package ssafy.everpet.domain.Map.service;

import ssafy.everpet.domain.Map.dto.MapInfoDTO;
import ssafy.everpet.domain.Map.dto.MapSaveDTO;

public interface MapService {

    void saveOrUpdateMap(MapSaveDTO mapSaveDTO);

    MapInfoDTO getMapInfo(int id);
}
