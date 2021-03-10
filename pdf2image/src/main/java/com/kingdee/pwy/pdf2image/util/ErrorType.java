package com.kingdee.pwy.pdf2image.util;

/**
 * @author wenwei_yang
 * @date 2021/1/26 17:29
 */
public enum ErrorType {
    /**
     * 编码值范围1100 - 1999  0100-0199
     */
    SUCCESS("0000", "成功"),
    FAIL("19991", "失败"),
    ;


    /**
     * 异常代码
     *
     * @author
     */
    public String errcode;

    /**
     * 异常信息
     *
     * @author
     */
    public String description;

    private ErrorType(String errcode, String description) {
        this.errcode = errcode;
        this.description = description;
    }

    /**
     * @return the errcode
     */
    public String getErrcode() {
        return errcode;
    }


    /**
     * @param errcode the errcode to set
     */
    public void setErrcode(String errcode) {
        this.errcode = errcode;
    }


    /**
     * @return the description
     */
    public String getDescription() {
        return description;
    }

    /**
     * @param description the description to set
     */
    public void setDescription(String description) {
        this.description = description;
    }

}

