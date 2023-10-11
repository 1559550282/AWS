package cn.tocute;


import com.alibaba.fastjson.JSON;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.stream.Collectors;

public class AwsUtilDemo {

    private static final String URI = "/model/anthropic.claude-v2/invoke";
    private static final String SERVICE = "bedrock"; // 替换为你要访问的AWS服务名称，例如：bedrock
    private static final String REGION = "us-east-1"; // 替换为你的AWS区域，例如：us-east-1
    private static final String ACCESS_KEY = "AKIAZSQxxxxD7B45"; // 替换为你的AWS密钥
    private static final String SECRET_KEY = "YaOMQPonHE8xxxxLK6E796d4"; // 替换为你的AWS访问密钥


    public static void main(String[] args) {
        String host = "bedrock-runtime."+REGION+".amazonaws.com";
        String uri = URI;
        String urlString = "https://" + host + uri;
        //String payload = "{\"prompt\":\"\\n\\nHuman:tell me a bedtime story\\n\\nAssistant:\",\"temperature\":0,\"top_p\":1,\"top_k\":1,\"max_tokens_to_sample\":100,\"stop_sequences\":[\"\\n\\nHuman:\"]}";

        Map<String,Object> requestMap = new HashMap<>();
        requestMap.put("prompt","Human:tell me a bedtime story\\n\\nAssistant:");
        requestMap.put("max_tokens_to_sample",100);
        String payload = JSON.toJSONString(requestMap);
        try {

            Date currentDate = new Date();
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMdd");
            String dateString = dateFormat.format(currentDate);
            String awsDate = getAwsDate(currentDate);

            Map<String, String> headers = new HashMap<>();
            headers.put("Content-Type", "application/json");
            headers.put("Host", host);
            headers.put("X-Amz-Content-Sha256", sha256(payload));
            headers.put("X-Amz-Date", awsDate);

            Map<String, String> sortedMap = new TreeMap<>(headers);

            String signedHeadersString = sortedMap.keySet().stream()
                    .map(String::toLowerCase)
                    .sorted()
                    .collect(Collectors.joining(";"));
            // 构建Canonical Request和签名
            String canonicalRequest = buildCanonicalRequest("POST", uri, "", sortedMap,signedHeadersString, payload);


            String algorithm = "AWS4-HMAC-SHA256";
            String credentialScope = dateString + '/' + REGION + '/' + SERVICE + "/aws4_request";
            String string2Sign = algorithm + '\n' +  awsDate + '\n' +  credentialScope + '\n' +  sha256(canonicalRequest);


            String signature = calculateSignature(string2Sign, SECRET_KEY, dateString,REGION,SERVICE);

            sortedMap.put("Authorization", "AWS4-HMAC-SHA256 Credential=" + ACCESS_KEY + "/" + credentialScope+", SignedHeaders=" + signedHeadersString + ", Signature=" + signature);

            String rs = HttpClientUtil.doJson(urlString, sortedMap, payload);

            System.out.println("请求结果："+rs);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }



    private static String sha256(String payload) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(payload.getBytes(StandardCharsets.UTF_8));

            // 将字节数组转换为十六进制字符串
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }

    private static String buildCanonicalRequest(String method, String uri, String query, Map<String, String> headers,String signedHeadersString, String payload) {
        StringBuilder canonicalHeadersBuilder = new StringBuilder();
        canonicalHeadersBuilder.append(method).append("\n");
        canonicalHeadersBuilder.append(uri).append("\n");
        canonicalHeadersBuilder.append(query).append("\n");
        for (Map.Entry<String, String> entry : headers.entrySet()) {
            canonicalHeadersBuilder.append(entry.getKey().toLowerCase()).append(":").append(entry.getValue().trim()).append("\n");
        }
        canonicalHeadersBuilder.append("\n");
        canonicalHeadersBuilder.append(signedHeadersString).append("\n");
        canonicalHeadersBuilder.append(sha256(payload));
        return canonicalHeadersBuilder.toString();
    }



    private static String calculateSignature(String stringToSign, String secretKey, String dateStamp, String region, String serviceName) {
        try {

            byte[] kSecret = ("AWS4" + secretKey).getBytes(StandardCharsets.UTF_8);
            byte[] kDate = HmacSHA256(dateStamp, kSecret);
            byte[] kRegion = HmacSHA256(region, kDate);
            byte[] kService = HmacSHA256(serviceName, kRegion);
            byte[] signingKey = HmacSHA256("aws4_request", kService);

            byte[] signature = HmacSHA256(stringToSign, signingKey);
            return bytesToHex(signature);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    private static byte[] getSignatureKey(String key, String dateStamp, String regionName, String serviceName) throws Exception {
        byte[] kSecret = ("AWS4" + key).getBytes(StandardCharsets.UTF_8);
        byte[] kDate = HmacSHA256(dateStamp, kSecret);
        byte[] kRegion = HmacSHA256(regionName, kDate);
        byte[] kService = HmacSHA256(serviceName, kRegion);
        return HmacSHA256("aws4_request", kService);
    }

    private static byte[] HmacSHA256(String data, byte[] key) throws Exception {
        Mac sha256Hmac = Mac.getInstance("HmacSHA256");
        SecretKeySpec secretKey = new SecretKeySpec(key, "HmacSHA256");
        sha256Hmac.init(secretKey);
        return sha256Hmac.doFinal(data.getBytes(StandardCharsets.UTF_8));
    }

    private static String bytesToHex(byte[] bytes) {
        StringBuilder result = new StringBuilder();
        for (byte b : bytes) {
            result.append(String.format("%02x", b));
        }
        return result.toString();
    }

    public static String getAwsDate(Date date ){
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMdd'T'HHmmss'Z'");
        dateFormat.setTimeZone(TimeZone.getTimeZone("UTC")); // 设置时区为UTC
        // 使用 SimpleDateFormat 格式化日期对象为字符串
        return dateFormat.format(date);
    }


}
