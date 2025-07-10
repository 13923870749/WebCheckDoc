# 后端服务（FastAPI）

## 启动方式

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 启动服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. 健康检查

访问 http://localhost:8000/ping 应返回 {"message": "pong"} 