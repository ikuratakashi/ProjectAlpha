import cv2
import numpy as np
from picamera2 import Picamera2

# Picamera2のセットアップ
camera = Picamera2()
camera_config = camera.create_video_configuration(main={"size": (640, 480)})
camera.configure(camera_config)
camera.start()
print("Picamera2のセットアップ 完了")

# 仮想カメラ用のVideoWriter
width, height = 640, 480  # 解像度
fps = 30  # フレームレート
isColor = True #カラーかどうか
pipeline = "appsrc ! videoconvert ! videoscale ! video/x-raw,format=YUY2 ! v4l2sink device=/dev/video50"
out = cv2.VideoWriter(pipeline,cv2.CAP_GSTREAMER, 0, fps, (width, height),isColor)

print("仮想カメラ用のVideoWriter 完了")

try:
    while True:
        # フレームをキャプチャ
        frame = camera.capture_array()
        frame = frame[:,:,:3]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 四角形を描画
        start_point = (50, 50)  # 四角形の始点
        end_point = (200, 200)  # 四角形の終点
        color = (0, 255, 0)  # 四角形の色 (BGRフォーマット)
        thickness = 3  # 四角形の線の太さ
        try:
            cv2.rectangle(frame, start_point, end_point, color, thickness)
        except Exception as e:
            print(f"error:{e}")

        # 仮想カメラに映像を送信
        out.write(frame)
        #del frame

except KeyboardInterrupt:

    print("Streaming stopped")

finally:
    print("Stop 開始")
    camera.stop()
    print("Stop 完了")
    print("release 開始")
    out.release()
    print("release 完了")
