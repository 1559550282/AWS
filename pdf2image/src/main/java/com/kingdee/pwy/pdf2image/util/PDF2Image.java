package com.kingdee.pwy.pdf2image.util;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.encryption.InvalidPasswordException;
import org.apache.pdfbox.rendering.PDFRenderer;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

/**
 * 将PDF转化为图片工具类
 *
 * @author wenwei_yang
 * @ClassName PDF2Image
 * @Package com.kingdee.util
 * @date 2020/12/23 17:02
 */
public class PDF2Image {
    private static final Log log = LogFactory.getLog(PDF2Image.class);

    public static final float RENDER_IMAGE_SCALE = 1.3f;

    private PDF2Image() {
    }

    /**
     * 将PDF转成多张图片
     *
     * @param filePath 文件路径
     * @param type     图片类型
     * @return java.io.File[]
     * @author wenwei_yang
     * @date 2020/12/23 17:02
     */
    public static File[] pdf2image(String filePath, String type) {
        File file = new File(filePath);
        if (!file.isFile()) {
            log.error(String.format("文件%s不存在", filePath));
            return new File[0];
        }
        try (PDDocument doc = PDDocument.load(file)) {
            log.info("PDDocument.load");
            PDFRenderer renderer = new PDFRenderer(doc);
            log.info("new PDFRenderer");
            int pageCount = doc.getNumberOfPages();
            log.info(String.format("该pdf共有%d页", pageCount));
            for (int i = 1; i <= pageCount; i++) {
                long cur = System.currentTimeMillis();
                BufferedImage image = renderer.renderImage(i - 1, RENDER_IMAGE_SCALE);
                log.info("耗时:" + (System.currentTimeMillis() - cur));
                String imagePath = file.getParent() + File.separator + Utils.getFileNameNoSuffix(filePath)
                        + '_' + i + '.' + type;
                log.info("生成临时图片" + imagePath);
                ImageIO.write(image, type, new File(imagePath));
                log.info("生成临时图片完成" + imagePath);
            }
            File[] images = file.getParentFile().listFiles(pathname -> pathname.isFile()
                    && pathname.getName().toLowerCase().endsWith('.' + type));
            if (images == null) return new File[0];
            log.info(String.format("已生成临时图片%d张", images.length));
            return images;
        } catch (InvalidPasswordException e) {
            log.error("访问pdf密码错误", e);
        } catch (IOException e) {
            log.error(e.getMessage(), e);
        }
        return new File[0];
    }
}
