#最終変更日6月21日
import SampleReadCardList
import IdReference
import CreateCsv

#csvファイルの読み込み
SampleReadCardList.read()

#print(type(IdReference.refer()))

#csvファイルに書き込み
CreateCsv.create(IdReference.refer())
