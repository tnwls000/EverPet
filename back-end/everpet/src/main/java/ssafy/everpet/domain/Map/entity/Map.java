package ssafy.everpet.domain.Map.entity;

import ssafy.everpet.domain.Map.dto.MapSaveDTO;
import ssafy.everpet.domain.User.entity.User;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
public class Map {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    private int width;
    private int height;
    private double resolution;

    @ElementCollection
    @CollectionTable(name = "map_data", joinColumns = @JoinColumn(name = "map_id"))
    @Column(name = "data", columnDefinition = "smallint")
    @Builder.Default
    private List<Short> data = new ArrayList<>();

    private double positionX;
    private double positionY;
    private double positionZ;

    private double orientationX;
    private double orientationY;
    private double orientationZ;
    private double orientationW;

    // ==연관관계 메서드== //
    public void setUser(User user) {
        this.user = user;
        user.setMap(this);
    }

    public void updateMap(MapSaveDTO mapSaveDTO, List<Short> shortList) {
        this.width = mapSaveDTO.getWidth();
        this.height = mapSaveDTO.getHeight();
        this.resolution = mapSaveDTO.getResolution();
        this.data = shortList;
        this.positionX = mapSaveDTO.getPositionX();
        this.positionY = mapSaveDTO.getPositionY();
        this.positionZ = mapSaveDTO.getPositionZ();
        this.orientationX = mapSaveDTO.getOrientationX();
        this.orientationY = mapSaveDTO.getOrientationY();
        this.orientationZ = mapSaveDTO.getOrientationZ();
        this.orientationW = mapSaveDTO.getOrientationW();
    }
}
