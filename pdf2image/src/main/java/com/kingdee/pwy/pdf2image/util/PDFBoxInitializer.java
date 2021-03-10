package com.kingdee.pwy.pdf2image.util;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.encryption.InvalidPasswordException;
import org.apache.pdfbox.rendering.PDFRenderer;

import java.io.File;

/**
 * PDF BOX 初始化单例
 *
 * @author wenwei_yang
 * @ClassName PDFBoxInitializer
 * @Package com.kingdee.pwy.pdf2image
 * @date 2021/1/14 18:16
 */
public class PDFBoxInitializer {
    private static final Log log = LogFactory.getLog(PDFBoxInitializer.class);

    public void init() {
        System.setProperty("pdfbox.fontcache", "/opt/fonts-cache/");
        File file = new File("/opt/init/init_file.pdf");
        try (PDDocument doc = PDDocument.load(file)) {
            PDFRenderer renderer = new PDFRenderer(doc);
            int pageCount = doc.getNumberOfPages();
            for (int i = 1; i <= pageCount; i++) {
                renderer.renderImage(i - 1, PDF2Image.RENDER_IMAGE_SCALE);
            }
        } catch (InvalidPasswordException e) {
            log.error("访问pdf密码错误", e);
        } catch (Exception e) {
            log.error(e.getMessage(), e);
        }
    }

    private PDFBoxInitializer() {

    }

    private static class SingletonHolder {
        private static final PDFBoxInitializer instance = new PDFBoxInitializer();
    }

    public static PDFBoxInitializer getInstance() {
        return SingletonHolder.instance;
    }
}
