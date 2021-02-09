发票云收票子模块无服务器改造</br>
============================================
### 背景描述<br>
###### 发票云收票子模块<br>
###### 随着集团上云步伐的加速，云之家积极寻求无接触部署方案提升实施效率。金山云因不支持对挂载卷和启动盘构造完整虚拟机镜像，同时无一键部署功能，因此金山云上系统部署效率无法提升。
###### AWS的cloudformation支持对计算资源、网络资源、安全的自动部署；AMI镜像可以将现有的基于EC2环境部署打包；从而可以提升客户试用环境、生产环境的部署效率。
### 改造前后架构对比<br>

### 部署架构<br>
<img src="https://github.com/1559550282/AWS/blob/main/piaozoneDemo-sam-build/image/architecture.png" width="775" alt="架构图" /><br>
### 代码说明<br>
###### 参见：CreatevpcEC2.json <br>

### 效果展示<br>
###### <a href="https://www.bilibili.com/video/BV1JV411b7mK/" title="收票子模块serverless改造"><img src="{image-url}" alt="Alternate Text" /></a>

