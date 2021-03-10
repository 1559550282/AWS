package com.kingdee.pwy.pdf2image.model;

import com.kingdee.pwy.pdf2image.util.Utils;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.util.List;

/**
 * @author wenwei_yang
 * @ClassName InvoicePDFUploadResp
 * @Package com.kingdee.model.aws
 * @Description
 * @date 2020/12/29 14:01
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class InvoicePDFUploadResp extends BaseResult {
    private String storageUrl;

    private List<String> snapshotPreUrls;

    public String getSnapshotPreUrl() {
        if (snapshotPreUrls != null && !snapshotPreUrls.isEmpty()) {
            String first = snapshotPreUrls.get(0);
            String ext = Utils.extractFileExtension(first);
            String firstFlag = "_1." + ext;
            for (String snapshotPreUrl : snapshotPreUrls) {
                if (snapshotPreUrl.contains(firstFlag)) {
                    return snapshotPreUrl;
                }
            }
        }
        return "";
    }
}
