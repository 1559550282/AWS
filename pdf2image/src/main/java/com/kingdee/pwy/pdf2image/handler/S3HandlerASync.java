package com.kingdee.pwy.pdf2image.handler;

import com.alibaba.fastjson.JSON;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import com.amazonaws.services.lambda.runtime.events.models.s3.S3EventNotification;
import com.kingdee.pwy.pdf2image.constant.Constants;
import com.kingdee.pwy.pdf2image.util.PDFBoxInitializer;
import com.kingdee.pwy.pdf2image.util.PDF2Image;
import com.kingdee.pwy.pdf2image.util.Utils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;
import software.amazon.awssdk.http.apache.ApacheHttpClient;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.File;
import java.util.List;

/**
 * S3触发异步方法
 *
 * @author wenwei_yang
 * @ClassName HandlerSync
 * @Package com.kingdee.pwy.pdf2image
 * @date 2021/1/26 17:29
 */
public class S3HandlerASync implements RequestHandler<S3Event, String> {
    private static final Log log = LogFactory.getLog(S3HandlerASync.class);

    private static final S3Client s3;

    static {
        s3 = S3Client.builder()
                .region(Region.of(Utils.getProperty(Constants.REGION_KEY)))
                .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
                .httpClientBuilder(ApacheHttpClient.builder().maxConnections(1000))
                .build();
        PDFBoxInitializer.getInstance().init();
    }

    /**
     * @param s3Event 1
     * @param context 2
     * @return java.lang.String
     * @Description S3事件处理
     * @author wenwei_yang
     * @date 2020/12/23 16:59
     */
    public String handleRequest(S3Event s3Event, Context context) {
        //指定字体缓存文件路径
        System.setProperty("pdfbox.fontcache", "/opt/fonts-cache/");
        List<S3EventNotification.S3EventNotificationRecord> records = s3Event.getRecords();
        log.info(String.format("接收到的S3数据为%s", JSON.toJSONString(s3Event)));
        log.info(String.format("接收到的context数据为%s", JSON.toJSONString(context)));
        for (S3EventNotification.S3EventNotificationRecord record : records) {
            String bucketName = record.getS3().getBucket().getName();
            String key = record.getS3().getObject().getUrlDecodedKey();
            GetObjectRequest getObjectRequest = GetObjectRequest.builder()
                    .bucket(bucketName)
                    .key(key)
                    .build();
            File pdfTmpPath = Utils.getFileTmpPath(key);
            log.info("===========AbsolutePath:" + pdfTmpPath.getAbsolutePath());
            //从S3下载刚上传的PDF文件到本地缓存
            s3.getObject(getObjectRequest, pdfTmpPath.toPath());
            File[] images = PDF2Image.pdf2image(pdfTmpPath.getAbsolutePath(), Constants.IMG_TYPE);
            if (images.length == 0) {
                log.error("转化图片失败，图片生成数为0");
                return "failed";
            }
            for (File srcImage : images) {
                String targetImgKey = key.substring(0, key.lastIndexOf(File.separator) + 1) + srcImage.getName();
                Utils.uploadFile(s3, Utils.getProperty(Constants.INVOICE_PDF_SNAPSHOT_STORAGE_BUCKET_KEY), targetImgKey, srcImage);
            }
            log.info(String.format("删除临时pdf %s %s", pdfTmpPath.getAbsolutePath(), pdfTmpPath.delete()));
            log.info(String.format("删除临时文件夹%s %s", pdfTmpPath.getParent(), pdfTmpPath.getParentFile().delete()));
        }
        return "success";
    }

    /**
     * @param s3
     * @return void
     * @Description 上传字体缓存到S3
     * @author wenwei_yang
     * @date 2020/12/31 22:21
     */
    private void uploadFontCache(S3Client s3) {
        PutObjectRequest objectRequest = PutObjectRequest.builder()
                .bucket(Utils.getProperty(Constants.INVOICE_PDF_SNAPSHOT_STORAGE_BUCKET_KEY))
                .key("fonts-cache/.pdfbox.cache")
                .build();
        String path = System.getProperty("pdfbox.fontcache");
        File cache = new File(path, ".pdfbox.cache");
        log.info("字体缓存文件是否存在：" + cache.exists());
        if (cache.exists()) {
            log.info("上传font cache到S3……" + path + ".pdfbox.cache");
            s3.putObject(objectRequest, cache.toPath());
        }
    }
}
