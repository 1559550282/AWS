xxx收票子模块无服务器改造</br>
============================================
### 背景描述<br>
###### xxx收票子模块基于Springcloud构建，主要用于移动端发票上传，发票识别，ERP前端展示的处理流程。系统在高并发场景运行时偶尔发生宕机事件。<br>
###### 采用AWS serverless改造，通过使用托管服务的原生功能可以简化系统架构，实现自动扩展，减少人工运维，提升系统稳定性的目标。<br>
### 改造前后架构对比<br>
###### 原系统架构，采用ERP前端与socketIO建立websocket连接，实现发票信息推送； 采用RabbitMQ实现socketio与发票识别模块的进程间通信。为简化系统设计，一次报销过程对应一个RabbitMQ队列。RabbitMQ为单点部署，应用上尚未支持集群扩展。实际运行过程中，在高并发场景RabbitMQ队列超出上限，导致系统挂起<br>
<img src="https://github.com/1559550282/AWS/blob/main/piaozoneDemo-sam-build/image/origin-issue.png" width="675" alt="改造前" /><br>
###### 使用serverless改造，使用websockAPI替换原有的socketIO。ERP前端与之建立连接后，将connectID保存至dynamoDB；发票识别模块使用Lambda替换，完成识别后从DynamoDB获取connectID，可以直接向websocketAPI post消息，完成双向通讯<br>
<img src="https://github.com/1559550282/AWS/blob/main/piaozoneDemo-sam-build/image/ServerlessIntro.png" width="675" alt="改造后" /><br>
###### 方案优势：<br>
- 简化架构<br>
  Lambda向Websocket API直接Post请求，摒弃RabbitMQ消息通知机制，大幅简化业务逻辑<br>
- 提升稳定性<br>
  全部采用托管服务，避免单点故障和集群扩展操作.APIGateway & Lambda支持自动扩展及高并发突增<br>
- 简化运维<br>
  托管serverless服务，自动扩展，无server运维投入<br>
- 成本节省<br>
  按照调用次数/连接总分钟数收费，无业务调用不收费，避免预制成本<br>
### 部署架构<br>
<img src="https://github.com/1559550282/AWS/blob/main/piaozoneDemo-sam-build/image/architecture.png" width="775" alt="架构图" /><br>
### 代码说明<br>
###### stepfunction
<img src="https://github.com/1559550282/AWS/blob/main/piaozoneDemo-sam-build/image/Stepfunction.png" width="675" alt="stepfunction" /><br>

### 效果展示<br>
###### <a href="https://www.bilibili.com/video/BV1JV411b7mK/" title="收票子模块serverless改造"><img src="https://github.com/1559550282/AWS/blob/main/piaozoneDemo-sam-build/image/architecture.png" alt="Alternate Text" /></a>

