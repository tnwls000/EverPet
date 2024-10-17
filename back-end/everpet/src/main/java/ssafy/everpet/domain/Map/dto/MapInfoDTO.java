package ssafy.everpet.domain.Map.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MapInfoDTO {
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

    private String serialNumber;
}
