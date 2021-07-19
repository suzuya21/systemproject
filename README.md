# systemproject
## ラズパイGUI(クライアント)利用方法
- python
- ~~各種必要なライブラリ(覚えてないけど pyside2とrequestsとかは使ってるはず)~~
- requirements.txtの中身

をインストールしたあと
サーバのIPアドレスに合わせて*Raspberrypi/GUI/tusin.py*を変更し，
### Linuxの場合
```shell
# レポジトリのディレクトリへ移動してから
sh ./run.sh # 引数として 1(ダウンロード),2(アップロード),etc(出席管理画面)
```

### 他
```shell
# RepositoryRoot はクローンしたレポジトリのパス
cd $RepositoryRoot/Raspberrypi/GUI
python Download.py
```

