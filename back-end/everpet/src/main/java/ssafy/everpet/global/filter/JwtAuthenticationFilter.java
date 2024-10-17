package ssafy.everpet.global.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.filter.OncePerRequestFilter;
import ssafy.everpet.domain.User.entity.CustomUserDetails;
import ssafy.everpet.domain.User.repository.UserRepository;
import ssafy.everpet.global.exception.CustomException;
import ssafy.everpet.global.exception.ErrorCode;
import ssafy.everpet.global.util.JwtTokenUtil;

import java.io.IOException;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final UserRepository userRepository;
    private final JwtTokenUtil jwtTokenUtil;

    private static final List<String> EXCLUDED_PATHS = List.of(
            "/user/validate-id",
            "/user/login",
            "/user/find-id",
            "/user/find-password",
            "/email/**",
            "/robot/verify",
            "/diary/raspberry"
    );

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        String path = request.getRequestURI();
        String method = request.getMethod();

        if (path.equals("/user") && method.equalsIgnoreCase("POST")) {
            return true;
        }

        if (path.equals("/robot") && method.equalsIgnoreCase("POST")) return true;

        for (String excludedPath : EXCLUDED_PATHS) {
            if (path.matches(excludedPath.replace("**", ".*"))) {
                return true;
            }
        }

        return false;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        String accessToken = jwtTokenUtil.extractAccessToken(request).orElseThrow(() -> new CustomException(ErrorCode.JWT_NOT_FOUND_ACCESS_TOKEN));

        if (jwtTokenUtil.isBlackListed(accessToken)) throw new CustomException(ErrorCode.JWT_BLACKLISTED);

        if (jwtTokenUtil.validateToken(accessToken)) {
            if (jwtTokenUtil.isExpired(accessToken)) {
                int id = jwtTokenUtil.getUserIdFromToken(accessToken).orElseThrow(() -> new CustomException(ErrorCode.JWT_NULL_ID));
                String refreshToken = jwtTokenUtil.getRefreshToken(id).orElseThrow(() -> new CustomException(ErrorCode.JWT_NULL_REFRESH));

                if (jwtTokenUtil.validateToken(refreshToken)) {
                    if (!jwtTokenUtil.isExpired(refreshToken)) {
                        String newAccessToken = jwtTokenUtil.createAccessToken(id);
                        jwtTokenUtil.sendAccessToken(response, newAccessToken);
                        saveAuthentication(id);
                    } else throw new CustomException(ErrorCode.JWT_EXPIRED_REFRESH);
                }

            } else {
                int id = jwtTokenUtil.getUserIdFromToken(accessToken).orElseThrow(() -> new CustomException(ErrorCode.JWT_NULL_ID));
                saveAuthentication(id);
            }
        }

        filterChain.doFilter(request, response);

    }

    private void saveAuthentication(int id) {
        userRepository.findById(id).ifPresent(user -> {
            CustomUserDetails customUserDetails = new CustomUserDetails(user);

            Authentication authentication = new UsernamePasswordAuthenticationToken(
                    customUserDetails, null, customUserDetails.getAuthorities());

            log.info("Saving authentication: {}", authentication);

            SecurityContextHolder.getContext().setAuthentication(authentication);
        });
    }
}
