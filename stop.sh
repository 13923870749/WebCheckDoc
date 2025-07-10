#!/bin/bash

# 关闭前端服务
frontend_pid=$(ps aux | grep 'npm run dev' | grep -v grep | awk '{print $2}')
if [ -n "$frontend_pid" ]; then
  kill $frontend_pid
  echo "前端服务已关闭 (PID: $frontend_pid)"
else
  echo "未检测到前端服务进程"
fi

# 关闭后端服务
backend_pid=$(ps aux | grep 'uvicorn main:app' | grep -v grep | awk '{print $2}')
if [ -n "$backend_pid" ]; then
  kill $backend_pid
  echo "后端服务已关闭 (PID: $backend_pid)"
else
  echo "未检测到后端服务进程"
fi

echo "所有服务已关闭。" 