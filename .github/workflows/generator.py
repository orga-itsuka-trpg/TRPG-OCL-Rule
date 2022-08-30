import os
import sys

#header
#ログ一覧を含まないhtml部分 cssやら説明書きやらはこれとfooterに書く
#checkbox要素のcheckedを使ってCSSに開いたり閉じたりさせている
#paddingやmarginはよくわかっていない
header="""<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ログ一覧</title>
    <style>
      /* メニュー全体 */
      .menu {
        width: fit-content;
      }

      /* チェックボックスは非表示にする（内部的な Off/On の機能だけ利用する） */
      .menu input {
        display: none;
      }

      /* 開いた状態のサブメニュー */
      .menu input:checked + ul {
        display: block;
        width: fix-content;
        padding: 0rem 0rem 0rem 1rem;
      }

      /* 閉じた状態のサブメニュー */
      .menu ul {
        display: none;
        /* 下記は開閉によらず共通の設定 */
        background: #eee;
        list-style: none;
        margin: 0;
        padding: 0rem 0rem 0rem 1rem;
      }

      /* 親項目の装飾 */
      .menu label {
        display: block;
        margin: 0;
        padding: 0rem;
        background: #ddd;
        cursor: pointer;
      }

      .menu label:hover {
        background: #ccc;
      }
    </style>
  </head>
  <body>
    <h3>シャン卓のログをお前に教える</h3>
    <div class="menu">"""

#この間にul要素が入れ子になる感じで
example="""<label for="item4">項目4</label>
    <input type="checkbox" id="item4">
    <ul>
        <li>項目１－１
        <li>項目１－２
        <li>項目１－３お前に教えるooooooooooooooo
    </ul>
"""

#footer 以下略
footer="""    </div>
    <p>かっこいいCSS書けるシャンカーにこのページを託す…</p>
  </body>
</html>"""

#url
#リポジトリごとに変える
#オルガのとこなら
#https://orga-itsuka-trpg.github.io/TRPG-OCL-Rule/
#になるはず
url="https://shanshan1129.github.io/testGithubActions/"

#未整理なのでやらない
black_list_dir=['シャンTRPGログ2021_10_02まで']
black_list_file=['']

def main():
    #ワーキングディレクトリ(ルート想定)のログフォルダの存在チェック ない場合終了
    if not os.path.isdir('./ログ'):
        return
    print(header)
    generate_li('ログ','logItem')
    print(footer)

#ログのリストをログフォルダを再帰的に走査して入れ子になった<li>要素をprintする
#path ルートフォルダ(ログフォルダ)
#classID CSSで閉じる仕組みのために着ける
#addLI 最初の階層だけ<li>付けない IQ28のゴリ押し実装 ベストプラクティスくれ
def generate_li(path,classID,addLI=False):
    files = os.listdir(path)
    #引数のパスから得られるディレクトリとファイルの一覧を生成
    #ブラックリストの物及び頭に.がついている物(.keepなど)を除外
    files_dir = [f for f in files if (not f.startswith('.')) and (f not in black_list_dir) and os.path.isdir(os.path.join(path, f))]
    files_file = [f for f in files if (not f.startswith('.')) and (f not in black_list_file) and os.path.isfile(os.path.join(path, f))]

    #デバッグ用
    print(path,file=sys.stderr)
    print(files_dir,file=sys.stderr)
    print(files_file,file=sys.stderr)

    #html生成
    for i,dir in enumerate(files_dir):
        localClassID=classID+"-"+str(i)
        print(('<li>'if addLI else '')+'<label for="'+localClassID+'">'+dir+"</label>")#      <label for="item1">項目１</label>
        print('<input type="checkbox" id="'+localClassID+'">')#        <input type="checkbox" id="item3">
        print('<ul>')
        generate_li(path+"/"+dir,'logItem'+"-"+str(i),True)
        print('</ul>')

    for file in files_file:
        print('<li><a href="'+url+path+'/'+file+'" target="_blank" rel="noopener noreferrer">'+file+'</a>')

    return

#【最後に】
#見てないけど多分ゴリ押しのスクリプトを書いたおれはIQ5 ミルクちゃんできた！
#もっとまともなやり方存在する説濃厚に 私に代わっていい感じに書き直してくれ！
#わかったかミズゴロウ

if __name__ == "__main__":
    main() 