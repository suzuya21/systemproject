#最終変更日7月13日
#文字列を「:」で区切るプログラム
#characterに「'区切りたい文字'」を渡す
#例えば['07:42:30']は['07', '42', '30']に変換できる

def split(character):
    result = character.split(':')
    return result
