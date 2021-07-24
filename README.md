# systemproject
## 下準備
ラズパイのGUIを使うためにはまずPythonのライブラリをインストールする必要がある．
Python,pipはすでにインストールされている前提として
プラットフォームに合わせて，必要なライブラリをインストールする．
### Linuxの場合
```shell
# レポジトリのディレクトリへ移動してから
sh ./install.sh # 必要なライブラリをインストール
```

### Windowsの場合
```shell
# レポジトリのディレクトリへ移動してから
install.batをダブルクリック
```

## ラズパイGUI(クライアント)利用方法
必要なライブラリをインストールした後，
設定を行い
プラットフォームに合わせて以下のように実行する．
### Linuxの場合
```shell
# レポジトリのディレクトリへ移動してから
sh ./run.sh # 実行
```

### Windowsの場合
```shell
# レポジトリのディレクトリへ移動してから
run.batをダブルクリック
```

### 設定
クライアントを使用する前にサーバのIPアドレスを設定する必要がある．
サーバマシンから
```sh
ifconfig # Linux
ipconfig # Windows
```
を実行するなどして
サーバのIPアドレスを確認し，
そのIPアドレスをRaspberrypi/GUI/tusin.pyのserverIP変数に記載する．
例
```python
serverIP = '192.168.1.11'
```

## サーバー利用方法
~~実際はnginxのインストールとその設定が必要だが，簡単のためインストールは省略する．~~

docker上ですべてを行う．
### 必要なソフトウェア
- ~~python~~
- ~~mariadb~~
- ~~nginx~~
- docker
    - nginxコンテナ(python3.7)
    - mariadbコンテナ
    - phpmyadminコンテナ

### dockerのインストール
```sh
sudo apt install docker docker-compose # ubuntu,debian系
sudo zypper install docker docker-compose # opensuse
sudo pacman -S docker docker-compose # archlinux系
```
windowsの場合
[docker公式サイト](https://www.docker.com/products/docker-desktop)
からインストーラをダウンロードし，
[docker公式ドキュメント](https://docs.docker.jp/docker-for-windows/wsl.html)
を参考にインストールする

```sh
docker -v
# -> Docker version 20.10.7, build f0df35096d
docker-compose -v
# -> docker-compose version 1.29.2, build unknown
```
を実行し，dockerとdocker-composeコマンドが利用可能なことを確認する．

```sh
docker-compose up -d --build
```
を実行することで，システムで使用するnginxとmariadbとphpmyadminのイメージがダウンロードされ，サーバが実行される．

ブラウザで[http://*ipadress*:13431/](http://ipadress:13431/)にアクセスし，ログインページが返されたら成功

