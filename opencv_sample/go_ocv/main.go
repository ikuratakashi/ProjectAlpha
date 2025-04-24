package main

import (
	"fmt"
	"image"
	"image/color"
	"os"
	"os/signal"
	"syscall"

	"gocv.io/x/gocv"
)

func main() {
	// カメラの設定
	deviceID := 0 // カメラデバイスのID
	width, height := 640, 480
	fps := 30
	isColor := false
	//fourcc := int('Y')<<24 | int('U')<<16 | int('Y')<<8 | int('2')

	// GStreamerパイプラインの設定
	pipeline := "appsrc ! videoconvert ! videoscale ! video/x-raw,format=YUY2 ! v4l2sink device=/dev/video50"

	writer, err := gocv.VideoWriterFile(pipeline, "", float64(fps), width, height, isColor)
	if err != nil {
		fmt.Printf("Error opening video writer: %v\n", err)
		return
	}
	defer writer.Close()

	webcam, err := gocv.VideoCaptureDevice(deviceID)
	if err != nil {
		fmt.Printf("Error opening webcam: %v\n", err)
		return
	}
	defer webcam.Close()

	fmt.Println("仮想カメラのセットアップ 完了")

	// フレームを処理
	frame := gocv.NewMat()
	defer frame.Close()

	// シグナルをキャッチして終了処理を行う
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigs
		fmt.Println("\nStreaming stopped")
		os.Exit(0)
	}()

	for {
		if ok := webcam.Read(&frame); !ok {
			fmt.Println("Error reading from webcam")
			continue
		}
		if frame.Empty() {
			continue
		}

		// カラーかグレースケールに変換
		if !isColor {
			gocv.CvtColor(frame, &frame, gocv.ColorBGRToGray)
		}

		// 四角形を描画
		//startPoint := image.Pt(50, 50)
		//endPoint := image.Pt(200, 200)
		//color := gocv.NewScalar(0, 255, 0, 0) // 緑色
		
		thickness := 3

		rect := image.Rect(50,50,200,200)
		col := color.RGBA{R:0,G:255,B:0,A:255}
		gocv.Rectangle(&frame, rect, col, thickness)

		// 仮想カメラに映像を送信
		if err := writer.Write(frame); err != nil {
			fmt.Println("Error writing to virtual camera")
			break
		}
	}
}