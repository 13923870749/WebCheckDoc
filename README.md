# 中文文档自动审核系统

## 项目简介
本项目旨在为本地部署场景下的中文技术文档（如检测方案、报告等）提供自动化审核、知识管理与智能增强能力，支持多角色权限、知识库管理、RAG智能审核、可视化结果展示等。

---

## 核心功能
- 用户注册/登录/权限管理（超级管理员/管理员/普通用户）
- 知识库管理（个人/公开库、标签、批量、版本、协作）
- 文档上传（PDF/Word/Markdown/TXT）、自动格式转换、元数据提取
- 审核任务（模板/自定义规则、进度反馈、分级、批注、导出）
- RAG智能审核（知识片段化、语义检索、知识增强）
- 审核结果可视化、导出、反馈
- 系统监控、日志、数据备份、安全加固

---

## 技术选型
- 前端：Vue3 + TypeScript + Ant Design Vue + Pinia + Vue Router + Axios + Vite
- 后端：FastAPI + SQLAlchemy + Alembic + PyJWT + Celery + loguru
- 数据库：MySQL 8.x
- 缓存/队列：Redis
- 文档处理：Pandoc + Apache Tika + PyMuPDF + Tesseract（OCR）
- 大模型：DeepSeek/ChatGLM（本地）、OpenAI API（云端）
- 向量数据库：Chroma（可升级FAISS/Milvus）
- 部署：Docker + Docker Compose
- 测试：pytest（后端）、Vitest（前端）
- 文档：MkDocs/Docsify

---

## 目录结构
```
项目根目录/
├── 需求分析.md
├── 个人开发计划.md
├── 技术选型.md
├── README.md
├── backend/           # 后端服务
├── frontend/          # 前端项目
├── docs/              # 其他文档（可选）
├── docker/            # 部署相关脚本
└── ...
```

---

## 快速启动
1. 克隆项目并进入目录
2. 配置 .env、数据库、依赖
3. 一键启动：`docker-compose up -d`
4. 访问前端：http://localhost:8080  后端API：http://localhost:8000

详细步骤见各子目录README或部署文档。

---

## 开发计划
详见《个人开发计划.md》，建议采用敏捷迭代，每轮聚焦可交付功能，持续优化。

---

## 贡献与联系方式
- 欢迎提交Issue、PR或建议
- 联系方式：xxx@example.com

---

## License
MIT 