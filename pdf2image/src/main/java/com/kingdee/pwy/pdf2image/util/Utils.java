package com.kingdee.pwy.pdf2image.util;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;

/**
 * 工具类
 *
 * @author wenwei_yang
 * @ClassName Utils
 * @Package com.kingdee.pwy.pdf2image
 * @date 2021/1/27 13:59
 */
public class Utils {
    private static final Log log = LogFactory.getLog(Utils.class);

    /**
     * 方法作用描述
     *
     * @param s3
     * @param bucketName
     * @param key
     * @param file
     * @return void
     * @author wenwei_yang
     * @date 2021/1/27 21:10
     */
    public static void uploadFile(S3Client s3, String bucketName, String key, File file) {
        log.info(String.format("上传临时文件%s到S3:%s", file.getAbsolutePath(), key));
        PutObjectRequest objectRequest = PutObjectRequest.builder()
                .bucket(bucketName)
                .key(key)
                .build();
        s3.putObject(objectRequest, file.toPath());
        log.info(String.format("删除临时文件%s %s", file.getAbsolutePath(), file.delete()));
    }

    /**
     * 获取配置
     *
     * @param key key
     * @return java.lang.String
     * @author wenwei_yang
     * @date 2021/1/28 23:45
     */
    public static String getProperty(String key) {
        Properties properties = new Properties();
        try (InputStream in = Utils.class.getClassLoader().getResourceAsStream("application.properties")) {
            properties.load(in);
        } catch (IOException e) {
            log.error(e);
            return "";
        }
        return properties.getProperty(key);
    }

    /**
     * 判断str是否为空
     *
     * @param str str
     * @return boolean
     * @author wenwei_yang
     * @date 2021/1/27 22:37
     */
    public static boolean isEmpty(String str) {
        if (null == str || str.trim().equals("") || "null".equals(str)) {
            return true;
        }
        return false;
    }

    /**
     * 生成KEY
     *
     * @param tenantNo     租户编号 没有则unknown-tenant
     * @param taxNo        企业税号（如果有）
     * @param fileName     文件名称
     * @param ifAppendDate 是否需要添加日期文件夹
     * @return java.lang.String
     * @author wenwei_yang
     * @date 2021/1/27 22:36
     */
    public static String generateKey(String tenantNo, String taxNo, String fileName, boolean ifAppendDate) {
        StringBuilder keyBuilder = new StringBuilder();
        //租户
        if (isEmpty(tenantNo)) {
            keyBuilder.append("unknown-tenant");
        } else {
            keyBuilder.append(tenantNo);
        }
        keyBuilder.append('/');

        //税号
        if (!isEmpty(taxNo)) {
            keyBuilder.append(taxNo);
            keyBuilder.append('/');
        }

        if (ifAppendDate) {
            //日期
            String today = new SimpleDateFormat("yyyy-MM-dd").format(new Date());
            keyBuilder.append(today);
            keyBuilder.append('/');
        }
        //文件名
        keyBuilder.append(fileName);
        return keyBuilder.toString();
    }

    /**
     * 根据key获取文件名
     *
     * @param key key
     * @return java.lang.String
     * @author wenwei_yang
     * @date 2020/12/23 17:03
     */
    public static String getFileName(String key) {
        return key.substring(key.lastIndexOf('/') + 1);
    }

    /**
     * 根据key生成本地临时路径存储
     *
     * @param key 文件key
     * @author wenwei_yang
     * @date 2020/12/23 17:03
     */
    public static File getFileTmpPath(String key) {
        String parentPath = File.separator + "tmp" + File.separator + getFileNameNoSuffix(key);
        File dic = new File(parentPath);
        if (!dic.exists()) {
            log.info(String.format("图片临时文件夹创建成功 %s", dic.mkdir()));
        }
        return new File(parentPath + File.separator + getFileName(key));
    }

    /**
     * 根据文件路径获取文件名不带文件后缀
     *
     * @param filePath 文件路径
     * @return java.lang.String
     * @author wenwei_yang
     * @date 2020/12/23 17:03
     */
    public static String getFileNameNoSuffix(String filePath) {
        int beginIndex = filePath.lastIndexOf(File.separator) + 1;
        int endIndex = filePath.lastIndexOf('.');
        if (endIndex == -1) {
            return filePath.substring(beginIndex);
        }
        return filePath.substring(beginIndex, endIndex);
    }

    /**
     * 获取文件后缀
     *
     * @param path path
     * @return java.lang.String
     * @author wenwei_yang
     * @date 2021/2/22 17:28
     */
    public static String extractFileExtension(String path) {
        int startIndex = path.lastIndexOf('.');
        if (startIndex == -1) {
            return null;
        }
        return path.substring(startIndex + 1);
    }

}
