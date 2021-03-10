package com.kingdee.pwy.pdf2image.constant;



/**
 * 常量类
 *
 * @author wenwei_yang
 * @ClassName Constants
 * @Package com.kingdee.pwy.pdf2image
 * @date 2021/1/27 15:17
 */
public final class Constants {

    private Constants() {

    }

    public static final String INVOICE_PDF_STORAGE_BUCKET_KEY = "aws.s3.buckets.invoice.pdf-bucket-name";

    public static final String INVOICE_PDF_SNAPSHOT_STORAGE_BUCKET_KEY = "aws.s3.buckets.invoice.pdf-snapshot-bucket-name";

    public static final String IMG_TYPE = "png";

    public static final String DOWNLOAD_URL_KEY = "aws.s3.pdf-download-url";

    public static final String REGION_KEY = "aws.s3.region";

}
