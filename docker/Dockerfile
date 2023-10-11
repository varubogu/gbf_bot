# base image
FROM python3:latest AS base-image

WORKDIR /usr/src/gbf_bot

COPY ../src/ ../config/ ./

ENV PYTHONPATH=./src  CONFIG_FOLDER=./config

RUN pip install --no-cache-dir -r requirements.txt

# debug image
FROM base-image AS debug-image

# デバッグ用ポート解放
# EXPOSE 5678

# デバッグ待機状態にする
# 未完成
# CMD [ "python", "-m", "debugpy", "--wait-for-client", "--listen", "5678", "-m" "bot" ]

# production image
FROM base-image AS production-image
CMD [ "python" "-m", "bot"]
