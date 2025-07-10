#!/bin/bash

# 创建 logs 目录
mkdir -p logs

# 启动前端服务
cd frontend
npm install &> ../logs/frontend_install.log
nohup npm run dev &> ../logs/frontend.log &
cd ..

echo "前端服务已启动，日志见 logs/frontend.log"

# 启动后端服务
cd backend
if [ -d "venv" ]; then
  source venv/bin/activate
else
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi
nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 &> ../logs/backend.log &
cd ..

echo "后端服务已启动，日志见 logs/backend.log"

echo "所有服务已启动。前端: http://localhost:5173  后端: http://localhost:8000" 