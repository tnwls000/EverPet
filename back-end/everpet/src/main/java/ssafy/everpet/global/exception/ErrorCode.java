package ssafy.everpet.global.exception;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@AllArgsConstructor
@Getter
public enum ErrorCode {
    // JSON
    JSON_PROCESSING_EXCEPTION(HttpStatus.BAD_REQUEST, "JSON 변환 과정 중 오류가 발생했습니다."),

    // OPEN AI
    OPENAI_FAIL_DOWNLOAD_IMAGE(HttpStatus.BAD_REQUEST, "DALLE의 url로부터 이미지 다운로드를 실패했습니다."),

    //JWT
    JWT_MALFORMED(HttpStatus.UNAUTHORIZED, "손상된 토큰입니다."),
    JWT_HEADER_STRING(HttpStatus.UNAUTHORIZED, "토큰 헤더의 문자열이 이상합니다."),
    JWT_NULL_REFRESH(HttpStatus.UNAUTHORIZED, "리프레시 토큰이 없습니다."),
    JWT_EXPIRED_REFRESH(HttpStatus.UNAUTHORIZED, "리프레시 토큰이 만료되었습니다."),
    JWT_EXPIRED(HttpStatus.UNAUTHORIZED, "만료된 토큰입니다."),
    JWT_INVALID(HttpStatus.UNAUTHORIZED, "유효하지 않은 토큰입니다."),
    JWT_NULL_ID(HttpStatus.UNAUTHORIZED, "Id가 없습니다"),
    JWT_NOT_FOUND_ACCESS_TOKEN(HttpStatus.UNAUTHORIZED, "헤더에 엑세스 토큰이 없습니다."),
    JWT_ERROR(HttpStatus.UNAUTHORIZED, "기타 JWT 에러"),
    JWT_BLACKLISTED(HttpStatus.UNAUTHORIZED, "이미 로그아웃된 사용자입니다."),

    // User
    INVALID_USER_ID(HttpStatus.BAD_REQUEST, "유효하지 않은 유저 아이디입니다."),
    INCORRECT_ID_OR_PASSWORD(HttpStatus.BAD_REQUEST, "아이디나 비밀번호가 일치하지 않습니다."),
    INCORRECT_PASSWORD(HttpStatus.CONFLICT, "비밀번호가 일치하지 않습니다."),
    DUPLICATE_USER_ID(HttpStatus.CONFLICT, "중복된 아이디가 존재합니다."),
    NOT_FOUND_NAME_AND_EMAIL(HttpStatus.NOT_FOUND, "해당 이름과 이메일에 맞는 회원이 존재하지 않습니다."),
    NOT_FOUND_USERID_AND_EMAIL(HttpStatus.NOT_FOUND, "해당 아이디와 이메일에 맞는 회원이 존재하지 않습니다."),
    DUPLICATE_EMAIL(HttpStatus.CONFLICT, "해당 이메일에 대한 회원이 이미 존재합니다."),

    // Diary
    NOT_MATCH_DIARY_AND_USER(HttpStatus.BAD_REQUEST, "해당 회원의 다이어리가 아닙니다."),
    INVALID_DIARY_ID(HttpStatus.BAD_REQUEST, "유효하지 않은 다이어리 아이디입니다."),

    // Map
    NOT_FOUND_MAP(HttpStatus.NOT_FOUND, "해당 회원의 지도를 찾을 수 없습니다."),

    // Friendship
    INVALID_FRIENDSHIP_TYPE_ID(HttpStatus.BAD_REQUEST, "유효하지 않은 친밀도 타입 아이디입니다."),
    INVALID_FRIENDSHIP_ACTION_ID(HttpStatus.BAD_REQUEST, "유효하지 않은 친밀도 행동 아이디입니다."),
    NOT_FOUND_FRIENDSHIP_TYPE(HttpStatus.NOT_FOUND, "친밀도 타입을 찾을 수 없습니다."),

    // SerialNumber
    INVALID_SERIAL_NUMBER_ID(HttpStatus.BAD_REQUEST, "유효하지 않은 시리얼 번호입니다."),
    NOT_FOUND_SERIAL_NUMBER(HttpStatus.BAD_REQUEST, "시리얼 번호를 찾을 수 없습니다."),
    DUPLICATE_SERIAL_NUMBER(HttpStatus.CONFLICT, "해당 시리얼 번호에 대한 회원과 로봇이 이미 등록되어 있습니다."),

    // Robot
    NOT_FOUND_ROBOT(HttpStatus.NOT_FOUND, "로봇을 찾을 수 없습니다.");

    private final HttpStatus httpStatus;
    private final String message;
}
