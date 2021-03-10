package org.apache.fontbox.util.autodetect;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

/**
 * 重写UnixFontDirFinder代码
 *
 * @author wenwei_yang
 * @ClassName UnixFontDirFinder
 * @Package org.apache.fontbox.util.autodetect
 * @date 2020/12/23 16:19
 */
public class UnixFontDirFinder extends NativeFontDirFinder {
    private static final Log log = LogFactory.getLog(UnixFontDirFinder.class);

    public UnixFontDirFinder() {
    }

    protected String[] getSearchableDirectories() {
        log.info("调用重写代码……");
        return new String[]{System.getProperty("user.home") + "/.fonts",
                "/usr/local/fonts", "/usr/local/share/fonts", "/usr/share/fonts",
                "/usr/X11R6/lib/X11/fonts", "/opt/chinese"};
    }
}