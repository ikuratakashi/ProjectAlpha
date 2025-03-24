# Raspberry Pi Zero 2 W のセットアップ

## OSのインストール

- 以下よりimagerをダウンロードしてメモリカードへインストール
https://www.raspberrypi.com/software/

OSについは以下を選択
- Raspberry Pi OS(64bit)

各種設定は任意で行う。

## aptのアップデート
```sh
sudo apt-get upgrade
sudo apt-get update
```
## テキストエディタ Vimのインストール
```sh
sudo apt install vim -f
```
## 使用するプロセッサ数を1つ少なくして全部占有状態を解消する
`~/.bashrc` へ以下を追加
```sh
export MAX_JOBS=$((nproc - 1))
```
### 変更内容の反映
```sh
source ~/.bashrc
```
## GUIの無効化
```sh
sudo systemctl set-default multi-user.target
sudo systemctl isolate multi-user.target
```
## GUIの有効化
```sh
sudo systemctl set-default graphical.target
sudo systemctl isolate graphical.target
```

**pyenvでpythonを動かすとカメラのライブラリが正常に動作しない為、pyenvのインストールおよびpythonのインストールは行わない**

## Pyenvのインストール
Pythonのバージョン管理ツール
### インストール
```
curl https://pyenv.run | bash
```
### シェルの設定
`~/.bashrc` `~/.zshrc` または使用しているシェルの設定ファイルに以下の行を追加します。
```sh
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
### シェルの再読み込み
```sh
source ~/.bashrc  
```
または 
```sh
source ~/.zshrc
```
### pythonインストール時に必要なパッケージのインストール
```sh
sudo apt install libssl-dev libbz2-dev libreadline-dev libsqlite3-dev zlib1g-dev libffi-dev gcc make
```
これをインストールしておかないとpythonのインストール時に失敗する。
### pythonのバージョン選択
以下のサイトでバージョンの状況を確認してからバージョンを選択する
特に指定が無ければ、featureのバージョンを選択するのが良い。

https://devguide.python.org/versions/

- feature：開発段階。
- prerelease：リリース間近。
- bugfix：安定板。機能追加あり。
- security：セキュリティ保障。機能追加・修正は行わない。
- end-of-life(eol)：バグ修正なし。セキュリティ保証なし。

### pythonのインストール
バックグラウンドでのインストール
途中でsshが切れてもインストールが動くようにするため
```sh
nohup pyenv install 3.12.9 &
```
20～30分でインストールは完了します。
### バージョン選択
- グローバルで選択する場合
```sh
pyenv global 3.12.9
```
- ローカルで選択する場合
```sh
pyenv local 3.12.9
```
- インストール済みのバージョンの確認方法
```sh
python --version
```

## VNCのインストール
### インストール
```
sudo apt install realvnc-vnc-server 
```

### VNCの有効化
以下を実行して設定変更画面を表示させる。
```
sudo raspi-config
```
1.Interface Options を選択
2.VNC を選択
3.Enable を選択

続けてディスプレイの解像度を設定

1.Display Options を選択
2.VNC Resolution を選択
3.使用したい解像度を選択（例: 1920x1080）

再起動が実行される

### ブラウザを表示した際のちらつきをなくす

※ちらつきをなくしても、起動に２分以上かかって使い物にならない。。。

`/boot/config.txt` に対して以下の部分を編集

（有効化）
```sh
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=16
```

（コメント化）
```sh
#display_auto_detect=1
```
## Gitのインストール
```
sudo apt-get install -y git
```

## momoのインストール

### カメラ映像の配信用
https://github.com/shiguredo/momo

- 公式サイトのインストール方法
https://github.com/shiguredo/momo/blob/develop/doc/SETUP_RASPBERRY_PI.md

### ダウンロード
- momoのGitHubにあるreleasesよりダウンロード
https://github.com/shiguredo/momo/releases

```sh
wget https://github.com/shiguredo/momo/releases/download/2024.1.1/momo-2024.1.1_raspberry-pi-os_armv8.tar.gz
```
- ダウンロードしたファイルを解凍
```sh
tar -xvzf momo-2024.1.1_raspberry-pi-os_armv8.tar.gz
```
- momoのバイナリに実行権限を与える
```sh
sudo chmod 777 momo
```

### ラズパイでの実行準備
https://github.com/shiguredo/momo/blob/develop/doc/SETUP_RASPBERRY_PI.md

- 動作に必要なパッケージをインストール
```sh
sudo apt-get install libnspr4 libnss3
sudo apt-get install libcamera0.4 libcamera-apps
sudo apt install python3-libcamera
```


- (この手順は不要となりました) カメラを有効にする

RaspberryPiのカメラモジュールをサポートするVideo4Linux2(V4L2)ドライバをロードしてカメラの最大解像度を指定する。

1. 設定ファイルを設置するフォルダを作成する(すでに存在しているかも)
```sh
mkdir /etc/modprobe.d
```
2. 設定ファイルを作成する
```sh
cd /etc/modprobe.d
```
```sh
sudo vim bcm2835-v4l2.conf
```

**フルパスでの修正コマンド**
```sh
sudo vim /etc/modprobe.d/bcm2835-v4l2.conf
```

3. 設定ファイルに以下の内容を記載する
```sh
options bcm2835-v4l2 max_video_width=640 max_video_height=480
```
4. 再起動

## momoの動作テスト

以下の公式サイトでのセットアップのmdより
https://github.com/shiguredo/momo/blob/develop/doc/SETUP_RASPBERRY_PI.md

- 実行
```sh
./momo --use-libcamera --no-audio-device test
```
実行すると以下のようなメッセージがターミナルに出力される。
```sh
[0:07:20.667683576] [5921]  INFO Camera camera_manager.cpp:327 libcamera v0.4.0+53-29156679
[0:07:20.873548652] [5935]  WARN RPiSdn sdn.cpp:40 Using legacy SDN tuning - please consider moving SDN inside rpi.denoise
[0:07:20.879683690] [5935]  INFO RPI vc4.cpp:447 Registered camera /base/soc/i2c0mux/i2c@1/ov5647@36 to Unicam device /dev/media2 and ISP device /dev/media0
[0:07:20.925543717] [5921]  INFO Camera camera_manager.cpp:327 libcamera v0.4.0+53-29156679
[0:07:20.995576297] [5942]  WARN RPiSdn sdn.cpp:40 Using legacy SDN tuning - please consider moving SDN inside rpi.denoise
[0:07:21.001559826] [5942]  INFO RPI vc4.cpp:447 Registered camera /base/soc/i2c0mux/i2c@1/ov5647@36 to Unicam device /dev/media2 and ISP device /dev/media0
[0:07:21.002848615] [5921]  INFO Camera camera.cpp:1202 configuring streams: (0) 640x480-YUV420
[0:07:21.003626002] [5942]  INFO RPI vc4.cpp:622 Sensor: /base/soc/i2c0mux/i2c@1/ov5647@36 - Selected sensor format: 640x480-SGBRG10_1X10 - Selected unicam format: 640x480-pGAA
```

- 動作確認用のhtmlで表示
実行が確認されたら、以下のようなURLでテスト用のhtmlが表示できる。

http://alpha.local:8080/html/test.html

- カメラデバイスを指定しての実行

1. 以下のコマンドでデバイスを調べる
```sh
v4l2-ctl --list-devices
```

2. 使用したいカメラの名前を取得する
 ```sh
 unicam (platform:3f801000.csi):
        /dev/video0
        /dev/media1

bcm2835-codec-decode (platform:bcm2835-codec):
        /dev/video10
        /dev/video11
        /dev/video12
        /dev/video18
        /dev/video31
        /dev/media3

bcm2835-isp (platform:bcm2835-isp):
        /dev/video13
        /dev/video14
        /dev/video15
        /dev/video16
        /dev/video20
        /dev/video21
        /dev/video22
        /dev/video23
        /dev/media0
        /dev/media2
 ```

 3. デバイス名を指定してmomoを実行
```sh
./momo --no-audio-device --video-device "VirtualCam" test
```
- ログ詳細を出力
 ```sh
./momo --log-level 0 --no-audio-device --video-device "VirtualCam" test
 ```

## OpenCV 

画像や動画を処理するためのライブラリ

### インストール
```sh
sudo apt install python3-opencv
```

## v4l2loopback

仮想カメラを作成するためのカーネルモジュール

### インストール
```sh
sudo apt install v4l2loopback-dkms
```

### 仮想カメラの作成

#### `/dev/video50` として作成
```sh
sudo modprobe v4l2loopback video_nr=50 exclusive_caps=0 card_label="alphaeye"
v4l2-ctl --list-devices
```
実行後に `v4l2-ctl --list-devices` コマンドを実行すると以下のように表示される
```sh
alphaeye (platform:v4l2loopback-000):
        /dev/video60
```
作成した仮想のカメラを削除するには
```sh
sudo modprobe -r v4l2loopback
```

## OpenCVを用いてlibcameraスタックと連携させる方法

OpenCV (cv2) を用いて libcamera スタックと連携する場合、問題が発生するのは一般的です。これは、Raspberry Pi OS Bullseye 以降でデフォルトとなった libcamera スタックが Video4Linux2 (V4L2) を介して OpenCV にカメラデータを提供しているため、いくつかの設定や制限に対応が必要になります。

OpenCV は libcamera のフレーム処理に完全には対応していません。
そのため、cap.read() でのフレーム取得が失敗することがあります。

/dev/video0 デバイスが V4L2 フレームバッファとして正しく動作していない場合、OpenCV はフレームを取得できません。

libcamera が正しく動作している場合、以下のように明示的に OpenCV でサポートさせる方法がある。

### Python ラッパーツールの活用：

- ライブラリのインストール
```sh
sudo apt install libcap-dev python3-picamera2
```

### gstremerのインストール

- 仮想デバイスの設定が上手くいかないのでgstreamerで行う為にインストール
```sh
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly python3-gst-1.0
```
### gstremerの実行

- 仮想カメラの設定を行うために、映像ストリームを供給
```sh
gst-launch-1.0 videotestsrc ! video/x-raw,width=640,height=480,framerate=30/1 ! v4l2sink device=/dev/video50
```

- 実行すると以下のような内容が表示される
```sh
Setting pipeline to PAUSED ...
Pipeline is PREROLLING ...
Pipeline is PREROLLED ...
Setting pipeline to PLAYING ...
Redistribute latency...
New clock: GstSystemClock
0:09:12.7 / 99:99:99.
```

又、以下のコマンドを実行するとデバイスの詳細が表示される
```sh
v4l2-ctl --device=/dev/video99 --list-formats-ext
```
実行結果
```sh
ioctl: VIDIOC_ENUM_FMT
        Type: Video Capture

        [0]: 'YUYV' (YUYV 4:2:2)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
```

## その他
- 指定したデバイスのフォーマットを表示する
```sh
ffmpeg -f v4l2 -list_formats all -i /dev/video0
```
- デバイスの一覧
```sh
v4l2-ctl --list-devices
```

## 映像配信までの手順
```sh
sudo modprobe v4l2loopback video_nr=50 exclusive_caps=0 card_label="alphaeye"
```
```sh
gst-launch-1.0 videotestsrc ! video/x-raw,width=640,height=480,framerate=30/1 ! v4l2sink device=/dev/video50
```
```sh
cd source/ProjectAlpha/opencv_sample
python sampl.py
```
```sh
cd momo
./momo --no-audio-device --video-device "alphaeye" test

./momo --log-level 0 --resolution=HD --force-i420 --hw-mjpeg-decoder=true --no-audio-device --video-device "alphaeye" test


```

http://alpha.local:8080/html/test.html