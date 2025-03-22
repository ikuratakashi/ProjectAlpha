import cv2
import numpy as np
from picamera2 import Picamera2

# Picamera2のセットアップ
camera = Picamera2()
camera_config = camera.create_video_configuration()
camera.configure(camera_config)
camera.start()

# 仮想カメラデバイスの設定
virtual_cam = "/dev/video99"

# 仮想カメラ用のVideoWriter
width, height = 640, 480  # 解像度
fps = 30  # フレームレート
fourcc = cv2.VideoWriter_fourcc(*'YUYV')
out = cv2.VideoWriter(virtual_cam, fourcc, fps, (width, height))

try:
    while True:
        # フレームをキャプチャ
        frame = camera.capture_array()

        # 四角形を描画
        start_point = (50, 50)  # 四角形の始点
        end_point = (200, 200)  # 四角形の終点
        color = (0, 255, 0)  # 四角形の色 (BGRフォーマット)
        thickness = 3  # 四角形の線の太さ
        cv2.rectangle(frame, start_point, end_point, color, thickness)

        # 仮想カメラに映像を送信
        out.write(frame)

except KeyboardInterrupt:
    print("Streaming stopped")

finally:
    camera.stop()
    out.release()