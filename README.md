# TJU_Cats
同济猫盟线上档案站。

目前活跃开发中，且部署在西伯利亚的破 VPS 上，较不稳定，故内测暂不开放

### 当前已实现：
- 分校区猫咪详细信息存档、查看，状态跟踪
- 在地图上添加、显示猫咪的日常活动范围
- 用户权限管理系统（尽管是 Django 自带的）
- 登录用户均可上传的猫咪相册，支持一图关联多猫
- 针对每只猫动态生成的操作列表，自动保存记录
- 错误日志即时微信推送
- 移动优先的响应式设计
- HTTPS

### 还未实现的功能——也可能不实现：
- 缓存系统
- 高级搜索
- 更舒服的前端相片查看及上传应用
- 视频播放上传
- 随猫咪状态动态优化的表单
- 高级统计可视化
- 面向领养人的网页系统
- 部署 CDN 存储与加速（需等待备案）
- 与操作整合的内部/半透明财务系统
- 一键部署脚本

## 开发路线
静态+反向代理: Nginx

动态部署: Apache2 + wsgi + Django (Python)

数据库: Mysql + ORM

前端: Bootstrap + jQuery