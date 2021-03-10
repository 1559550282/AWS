package com.kingdee.pwy.pdf2image.model;

import com.kingdee.pwy.pdf2image.util.ErrorType;

import java.io.Serializable;

/**
 * @author wenwei_yang
 * @date 2021/1/26 17:29
 */
public class BaseResult implements Serializable {
    /**
     * 序列号
     */
    protected static final long serialVersionUID = 1L;

    /**
     * 返回码
     */
    protected String errcode;

    /**
     * 返回描述
     */
    protected String description;

    /**
     * 对象信息
     */
    protected Object data;


    /**
     * 构造
     */
    public BaseResult() {
        this.errcode = ErrorType.SUCCESS.getErrcode();
        this.description = ErrorType.SUCCESS.getDescription();
    }

    /**
     * 构造
     *
     * @param errorType
     */
    public BaseResult(ErrorType errorType) {
        this.errcode = errorType.getErrcode();
        this.description = errorType.getDescription();
    }

    /**
     * @param errorType
     * @param data
     */
    public BaseResult(ErrorType errorType, Object data) {
        this.errcode = errorType.getErrcode();
        this.description = errorType.getDescription();
        this.data = data;
    }


    /**
     * @param errcode
     * @param description
     */
    public BaseResult(String errcode, String description) {
        this.errcode = errcode;
        this.description = description;
    }

    /**
     * @param errcode
     * @param description
     * @param data
     */
    public BaseResult(String errcode, String description, Object data) {
        this.errcode = errcode;
        this.description = description;
        this.data = data;
    }

    /**
     * @param @return 参数
     * @return String 返回类型
     * @throws
     * @Description TODO
     */
    public String getErrcode() {
        return errcode;
    }

    /**
     * @param @param errcode 参数
     * @return void 返回类型
     * @throws
     * @Description TODO
     */
    public void setErrcode(String errcode) {
        this.errcode = errcode;
    }

    /**
     * @param @return 参数
     * @return String 返回类型
     * @throws
     * @Description TODO
     */
    public String getDescription() {
        return description;
    }

    /**
     * @param @param description 参数
     * @return void 返回类型
     * @throws
     * @Description TODO
     */
    public void setDescription(String description) {
        this.description = description;
    }

    /**
     * @param @return 参数
     * @return Object 返回类型
     * @throws
     * @Description TODO
     */
    public Object getData() {
        return data;
    }

    /**
     * @param @param data 参数
     * @return void 返回类型
     * @throws
     * @Description TODO
     */
    public void setData(Object data) {
        this.data = data;
    }


}
