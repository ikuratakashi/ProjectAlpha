# GoでのOpenCVサンプル作成

## OpenCVのインストール

1. 依存関係のライブラリをインストール

```sh
sudo apt-get update 
sudo apt-get install -y build-essential pkg-config cmake libgtk-3-dev  libavcodec-dev  libavformat-dev
sudo apt-get install -y libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev 
sudo apt-get install -y gfortran openexr libatlas-base-dev libtbbmalloc2 libtbb-dev libdc1394-dev unzip yum 
sudo apt-get install -y qtbase5-dev qt5-qmake
```

2. GitHubからOpenCVのソースをクローン

```sh
git clone https://github.com/hybridgroup/gocv.git
```
クローンが成功すると`gocv`というフォルダが作成される。

3. コンパイルする準備をする

### MakeFileを修正
gocvのフォルダ内にある `MakeFile` を修正する

```sh
cd gocv
vim MakeFile
```

### 修正箇所

`build_raspi:` と `build_raspi_zero:` の段落にある `cmake` に以下を追加する

```sh
 -D WITH_GSTREAMER=ON
```

### ( 例 )

最後の方に `-D WITH_GSTREAMER=ON` が追加されている。
```sh
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_SHARED_LIBS=${BUILD_SHARED_LIBS} -D OPENCV_EXTRA_MODULES_PATH=$(TMP_DIR)opencv/opencv_contrib-$(OPENCV_VERSION)/modules -D BUILD_DOCS=OFF -D BUILD_EXAMPLES=OFF -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=ON -D BUILD_opencv_java=OFF -D BUILD_opencv_python=NO -D BUILD_opencv_python2=NO -D BUILD_opencv_python3=NO -D ENABLE_NEON=ON -D WITH_JASPER=OFF -D WITH_TBB=ON -D OPENCV_GENERATE_PKGCONFIG=ON -D WITH_FREETYPE=ON -D WITH_GSTREAMER=ON ..
```

### コンパイル & インストール

以下のコマンドを実行するとコンパイルとインストールが実行される。
gocvは結構な時間がかかるので、注意する。

```sh
make install
```


