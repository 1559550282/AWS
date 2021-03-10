package com.kingdee.pwy.pdf2image.handler;

import com.alibaba.fastjson.JSON;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import com.kingdee.pwy.pdf2image.constant.Constants;
import com.kingdee.pwy.pdf2image.model.InvoicePDFUploadResp;
import com.kingdee.pwy.pdf2image.util.ErrorType;
import com.kingdee.pwy.pdf2image.util.PDF2Image;
import com.kingdee.pwy.pdf2image.util.PDFBoxInitializer;
import com.kingdee.pwy.pdf2image.util.Utils;
import org.apache.commons.codec.binary.Base64;
import org.apache.commons.io.FileUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;
import software.amazon.awssdk.http.apache.ApacheHttpClient;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/**
 * api gateway触发同步方法
 *
 * @author wenwei_yang
 * @ClassName HandlerSync
 * @Package com.kingdee.pwy.pdf2image
 * @date 2021/1/26 17:29
 */
public class RestAPIHandlerSync implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {
    private static final Log log = LogFactory.getLog(RestAPIHandlerSync.class);

    private static final String ROOT_DIRECTORY = "SYNC/";

    private static final S3Client s3;

    static {
        log.info("环境是。。" + Utils.getProperty("aws.s3.buckets.invoice.pdf-bucket-name"));
        s3 = S3Client.builder()
                .region(Region.of(Objects.requireNonNull(Utils.getProperty(Constants.REGION_KEY))))
                .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
                .httpClientBuilder(ApacheHttpClient.builder().maxConnections(1000))
                .build();
        PDFBoxInitializer.getInstance().init();
    }

    @Override
    public APIGatewayProxyResponseEvent handleRequest(APIGatewayProxyRequestEvent apiGatewayProxyRequestEvent,
                                                      Context context) {
        APIGatewayProxyResponseEvent response = new APIGatewayProxyResponseEvent();
        InvoicePDFUploadResp resp = new InvoicePDFUploadResp();
        log.info(String.format("APIGatewayProxyRequestEvent %s", JSON.toJSONString(apiGatewayProxyRequestEvent)));
        log.info(String.format("Context %s", JSON.toJSONString(context)));


        boolean isBase64Encoded = apiGatewayProxyRequestEvent.getIsBase64Encoded();
        if (!isBase64Encoded) {
            //返回错误
            log.error(String.format("isBase64Encoded %s", false));
            resp.setErrcode(ErrorType.FAIL.errcode);
            resp.setDescription("文件传输格式出错，必须通过Base64 encode");
            return response.withBody(JSON.toJSONString(resp));
        }
        Map<String, String> params = apiGatewayProxyRequestEvent.getQueryStringParameters();
        String tenantNo = params.getOrDefault("tenantNo", "");
        String taxNo = params.getOrDefault("taxNo", "");
        String fileName = params.getOrDefault("fileName", "");
        boolean ifStoragePDF = Boolean.parseBoolean(params.getOrDefault("ifStoragePDF", "true"));
        String fileStream = apiGatewayProxyRequestEvent.getBody();
        //SYNC/租户编号/税号/日期/xxx.pdf
        String pdfKey = ROOT_DIRECTORY + Utils.generateKey(tenantNo, taxNo, fileName, true);
        //将文件流转化为本地pdf
        File pdfTmp = Utils.getFileTmpPath(pdfKey);
        byte[] decodeBase64 = Base64.decodeBase64(fileStream);
        try {
            FileUtils.writeByteArrayToFile(pdfTmp, decodeBase64);
        } catch (IOException e) {
            log.error(e);
            resp.setErrcode(ErrorType.FAIL.errcode);
            resp.setDescription("文件解析出错，具体请查看日志");
            return response.withBody(JSON.toJSONString(resp));
        }

        //将pdf转化为图片
        File[] images = PDF2Image.pdf2image(pdfTmp.getAbsolutePath(), Constants.IMG_TYPE);
        String pdfUrl = null;
        if (ifStoragePDF) {
            pdfUrl = String.format(Utils.getProperty(Constants.DOWNLOAD_URL_KEY),
                    Utils.getProperty(Constants.INVOICE_PDF_STORAGE_BUCKET_KEY), pdfKey);
            //上传pdf
            Utils.uploadFile(s3, Utils.getProperty(Constants.INVOICE_PDF_STORAGE_BUCKET_KEY), pdfKey, pdfTmp);
        }
        //上传图片
        List<String> snapshotUrls = new ArrayList<>();
        for (File img : images) {
            String imgKey = pdfKey.substring(0, pdfKey.lastIndexOf('/') + 1) + img.getName();
            Utils.uploadFile(s3, Utils.getProperty(Constants.INVOICE_PDF_SNAPSHOT_STORAGE_BUCKET_KEY), imgKey, img);
            snapshotUrls.add(String.format(Utils.getProperty(Constants.DOWNLOAD_URL_KEY),
                    Utils.getProperty(Constants.INVOICE_PDF_SNAPSHOT_STORAGE_BUCKET_KEY), imgKey));
        }

        //返回pdf和图片地址
        resp.setStorageUrl(pdfUrl);
        resp.setSnapshotPreUrls(snapshotUrls);
        resp.setErrcode(ErrorType.SUCCESS.errcode);
        resp.setDescription(ErrorType.SUCCESS.description);
        return response.withBody(JSON.toJSONString(resp));
    }
}
