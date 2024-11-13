# 使用 Python 3.11 的官方基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器的 /app 目录
COPY . .

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用程序运行的端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 启动 Flask 应用程序
CMD ["flask", "run"]