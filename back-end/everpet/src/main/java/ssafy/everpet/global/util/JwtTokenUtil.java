package ssafy.everpet.global.util;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import ssafy.everpet.domain.User.service.CustomUserDetailsService;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;

import java.security.Key;
import java.util.Date;
import java.util.Optional;

@Component
@RequiredArgsConstructor
@Slf4j
public class JwtTokenUtil {

    @Value("${JWT_SECRET_KEY}")
    private String jwtSecretKey;

    @Value("${JWT_ACCESS_TOKEN_PERIOD}")
    private Long accessTokenPeriod;

    @Value("${JWT_REFRESH_TOKEN_PERIOD}")
    private Long refreshTokenPeriod;

    @Value("${ACCESS_HEADER}")
    private String accessHeader;

    private static final String ACCESS_TOKEN_SUBJECT ="AccessToken";
    private static final String REFRESH_TOKEN_SUBJECT ="RefreshToken";
    private static final String PK = "pk";
    private static final String BEARER = "Bearer";

    private final CustomUserDetailsService customUserDetailsService;
    private final RedisUtil redisUtil;

    private Key getSigningKey() {
        return Keys.hmacShaKeyFor(jwtSecretKey.getBytes());
    }

    public String createAccessToken(int id) {
        Date now = new Date();
        return Jwts.builder()
                .setIssuedAt(now)
                .setExpiration(new Date(now.getTime() + accessTokenPeriod))
                .claim(PK, id)
                .signWith(getSigningKey())
                .compact();
    }

    public String createRefreshToken(int id) {
        Date now = new Date();
        return Jwts.builder()
                .setIssuedAt(now)
                .setExpiration(new Date(now.getTime() + refreshTokenPeriod))
                .claim(PK, id)
                .signWith(getSigningKey())
                .compact();
    }

    public void sendAccessToken(HttpServletResponse response, String accessToken) {
        response.setStatus(HttpServletResponse.SC_OK);
        response.setHeader(ACCESS_TOKEN_SUBJECT, accessToken);
        log.info("발급된 access token: {}", accessToken);
    }

    public void sendRefreshToken(int id, String refreshToken) {
        log.info("send refresh token: {}", refreshToken);
        redisUtil.setDataExpire(REFRESH_TOKEN_SUBJECT + id, refreshToken, refreshTokenPeriod);
    }

    public Optional<String> getRefreshToken(int id) {
        log.info("get refresh token method");
        return Optional.ofNullable(redisUtil.getData(REFRESH_TOKEN_SUBJECT + id));
    }

    public void deleteRefreshToken(int id) {
        redisUtil.deleteData(REFRESH_TOKEN_SUBJECT + id);
    }

    public Optional<String> extractAccessToken(HttpServletRequest request) {
        return Optional.ofNullable(request.getHeader(accessHeader))
                .filter(token -> token.contains(BEARER))
                .map(token -> token.replace(BEARER, ""));

    }

    public Optional<Integer> getUserIdFromToken(String token) {
        return Optional.ofNullable((Integer) Jwts.parserBuilder()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token)
                .getBody().get(PK));
    }

    public long getExpired(String token) {
        Claims claims = Jwts.parserBuilder()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token)
                .getBody();
        return claims.getExpiration().getTime();
    }

    public boolean isExpired(String token) {
        try {
            Jwts.parserBuilder().setSigningKey(getSigningKey()).build().parseClaimsJws(token);
        } catch (ExpiredJwtException expiredJwtException) {
            return true;
        }
        return false;
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder().setSigningKey(getSigningKey()).build().parseClaimsJws(token);
            return true;
        } catch (MalformedJwtException malformedJwtException) {
            throw new CustomException(ErrorCode.JWT_MALFORMED);
        } catch (InvalidClaimException invalidClaimException) {
            throw new CustomException(ErrorCode.JWT_INVALID);
        } catch (JwtException jwtException) {
            throw new CustomException(ErrorCode.JWT_ERROR);
        }
    }

    public void setBlackList(String accessToken, String msg) {
        long expired = this.getExpired(accessToken);
        redisUtil.setBlackList(accessToken, msg, expired);
    }

    public boolean isBlackListed(String token) {
        Optional<String> blackList = redisUtil.getBlackList(token);
        return blackList.isPresent();
    }
}
