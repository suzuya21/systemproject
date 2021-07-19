#最終変更日7月13日
#listに「履修者のデータ(list型)」, IDに「'比較したいID'」を渡す
#渡した履修者のデータとIDが比較された後, 結果がRegister(list型)に格納され返される
#履修者以外のIDがIDに渡された場合, Registerは空のリストとなる ⇒ Registerが空かどうかで履修者かどうか判断できる

#履修者のデータとIDを比較する関数
def idCompare(list, ID):
    Register = []
    for i in list:
        for j in i:
            #IDとlist[i][j]が一致すればループを抜ける
            if j == ID:
                Register = i
                break
    
    return Register