package ssafy.everpet.global.s3;

import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class S3Service {
    private final AmazonS3Client amazonS3Client;

    @Value("${cloud.aws.s3.bucket}")
    private String bucket;

    private static final String DIARY_IMG_DIR = "diary/";

    public String uploadDiaryImage(MultipartFile file) throws IOException {
        String originalFilename = file.getOriginalFilename();
        String extension = originalFilename != null ? originalFilename.substring(originalFilename.lastIndexOf(".") + 1) : "jpg";
        String uuidFileName = UUID.randomUUID() + "." + extension;
        String fileName = DIARY_IMG_DIR + uuidFileName;

        ObjectMetadata metadata = new ObjectMetadata();
        metadata.setContentLength(file.getSize());
        metadata.setContentType(file.getContentType());

        PutObjectRequest putRequest = new PutObjectRequest(bucket, fileName, file.getInputStream(), metadata);
        amazonS3Client.putObject(putRequest);

        return amazonS3Client.getUrl(bucket, fileName).toString();
    }

    public URL getFileUrl(String filePath) {
        return amazonS3Client.getUrl(bucket, filePath);
    }

}
