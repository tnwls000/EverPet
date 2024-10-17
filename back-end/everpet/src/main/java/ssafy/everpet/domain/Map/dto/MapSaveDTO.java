package ssafy.everpet.domain.Map.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class MapSaveDTO {
    private String userId;

    private int width;
    private int height;
    private double resolution;

    private short[] data;

    private double positionX;
    private double positionY;
    private double positionZ;

    private double orientationX;
    private double orientationY;
    private double orientationZ;
    private double orientationW;
}
