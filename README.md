# systemproject
# ラズパイGUI(クライアント)
ラズパイのGUIはsystemproject.zipとして配布している．
## 下準備
systemproject.zipを解凍する．
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
ラズパイのGUIは履修者データをダウンロードし，その履修者データを用いて出席管理を行い，そのデータをサーバにアップロードするために使用される．
必要なライブラリをインストールした後，
設定を行い
プラットフォームに合わせて以下のように実行し，表示される3つのボタンをクリックすることで各種機能が使用できる．
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

### ダウンロード
履修者データをダウンロードする．
この機能はクライアントマシンがサーバと同じネットワークに接続されているときに使用できる．
出席管理を行いたい科目のIDを選択し，ダウンロードボタンをクリックする．

### アップロード
出席データをアップロードする．
この機能はクライアントマシンがサーバと同じネットワークに接続されているときに使用できる．
アップロードしたい科目IDと授業回数をコンボボックスから選択肢，アップロードのボタンを押すことでその授業回数の出席データがサーバにアップロードされる．
アップロードが成功するとアップロードに使用した出席データのファイルを削除する．

### 出席管理メイン画面
出席管理を行う．
起動画面で出席管理を行いたい科目のIDと授業回数を選択し，開始ボタンを押すことで出席管理画面に遷移する．
このとき，出席管理を行いたい科目の履修者データがない場合は警告が表示されるので，ダウンロードGUIを起動し，その科目の履修者データをダウンロードする必要がある．
出席管理画面ではカードからIDを読み取った場合に規則時間と現在時刻を比較し，出席かどうかが表示される．(今回はターミナルでエンターキーを押すことでIDを読み取る．)
出席管理を終える場合は終了ボタンを押す．
この出席データをサーバにアップロードする場合はアップロードGUIを起動し，アップロードを行う．


# サーバ
サーバはsousei.zipとして配布している．
~~実際はnginxのインストールとその設定が必要だが，簡単のためインストールは省略する．~~

docker上ですべてを行う．
## 必要なソフトウェア
- ~~python~~
- ~~mariadb~~
- ~~nginx~~
- docker
    - nginxコンテナ(python3.7)
    - mariadbコンテナ
    - phpmyadminコンテナ

## dockerのインストール
### Linuxの場合
下記コマンドでだいたいインストールできるはず
```sh
sudo apt install docker docker-compose # ubuntu,debian系
sudo zypper install docker docker-compose # opensuse
sudo pacman -S docker docker-compose # archlinux系
```
インストール後に有効化する．
```sh
systemctl start docker # docker有効化
```

### windowsの場合
[docker公式サイト](https://www.docker.com/products/docker-desktop)
からインストーラをダウンロードし，
[docker公式ドキュメント](https://docs.docker.jp/docker-for-windows/wsl.html)
を参考にインストールする

インストールが完了したと思われる状態になったら，
```sh
docker -v
# -> Docker version 20.10.7, build f0df35096d
docker-compose -v
# -> docker-compose version 1.29.2, build unknown
```
を実行し，dockerとdocker-composeコマンドが利用可能なことを確認する．
実行できていない場合は一度再起動して，再び上記コマンドを実行してみる．
実行できない場合は要相談

## サーバの実行方法
sousei.zipを解凍後docker-compose.ymlのあるディレクトリに移動して，
```sh
docker-compose up -d --build
```
を実行することで，システムで使用するnginxとmariadbとphpmyadminのイメージがダウンロードされ，サーバが実行される．

ブラウザで[http://*ipadress*:13431/](http://ipadress:13431/)にアクセスし，ログインページが返されたら成功

