import os
import sys

header = """<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ログ一覧</title>
    <link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
    <style>
      /* メニュー全体 */
      .menu {
        width: fit-content;
      }

      /* 開いた状態のサブメニュー */
      .menu ul {
        display: block;
        width: fix-content;
        padding: 0rem 0rem 0rem 1rem;
        background: #eee;
        list-style: none;
        margin: 0;
      }

      /* 親項目の装飾 */
      .menu summary {
        display: block;
        margin: 0;
        padding: 0rem;
        background: #ddd;
        cursor: pointer;
      }

      .menu summary:hover {
        background: #ccc;
      }
    </style>
  <body>
    <h3>シャン卓のログをお前に教える</h3>
    <div class="menu">"""

#この間にul要素が入れ子になる感じで
example="""<details><summary>項目3</summary>
    <ul>
        <li>項目１－１
        <li>項目１－２
        <li>項目１－３お前に教えるoooooooooooooooa
    </ul>
    <details>
"""

#footer 以下略
footer="""    </div>
     <p>このページは<a href=https://github.com/ShanShan1129 target=_blank rel="noopener noreferrer">ShanShan1129</a>の非公式版なので<br>足りないログがある可能性も普通にあることを教える</p><p>とはいえログの抜けに気が付いた時はスレとかで報告上げてくれると助かるけどお前ら？</p>
  </body>
</html>"""

black_list_dir = []
black_list_file = []


# =========================
# ① ツリー構造を作る
# =========================
import re

def extract_year(name):
    """
    先頭のyyyymmddを検出して年を返す
    """
    match = re.match(r'^(\d{4})(\d{2})(\d{2})', name)
    if match:
        return match.group(1)
    return None


def build_tree(path):
    node = {
        "name": os.path.basename(path),
        "type": "dir",
        "children": []
    }

    try:
        files = os.listdir(path)
    except Exception as e:
        print(e, file=sys.stderr)
        return node

    files_dir = [
        f for f in files
        if not f.startswith('.') and
        f not in black_list_dir and
        os.path.isdir(os.path.join(path, f))
    ]

    files_file = [
        f for f in files
        if not f.startswith('.') and
        not f.endswith('.keep') and
        f not in black_list_file and
        os.path.isfile(os.path.join(path, f))
    ]

    files_dir.sort()
    files_file.sort()

    # 年ごとにまとめる用
    year_groups = {}

    # ===== ディレクトリ処理 =====
    for d in files_dir:
        full_path = os.path.join(path, d)
        year = extract_year(d)

        child_node = build_tree(full_path)

        if year:
            year_groups.setdefault(year, []).append(child_node)
        else:
            node["children"].append(child_node)

    # ===== ファイル処理 =====
    for f in files_file:
        full_path = os.path.join(path, f)
        year = extract_year(f)

        file_node = {
            "name": f,
            "type": "file",
            "path": full_path
        }

        if year:
            year_groups.setdefault(year, []).append(file_node)
        else:
            node["children"].append(file_node)

    # ===== 年ノードを追加 =====
    for year in sorted(year_groups.keys()):
        node["children"].append({
            "name": year,
            "type": "dir",
            "children": year_groups[year]
        })

    return node


# =========================
# ② ツリーからHTML生成
# =========================
def render_html(node, add_li=False):
    html = ""

    if node["type"] == "dir":
        if add_li:
            html += "<li>"

        html += f'<details><summary>{node["name"]}</summary>\n<ul>\n'

        for child in node["children"]:
            html += render_html(child, True)

        html += "</ul>\n</details>\n"

    else:  # file
        if add_li:
            html += "<li>"
        html += f'<a href="{node["path"]}" target="_blank" rel="noopener noreferrer">{node["name"]}</a>\n'

    return html


def main():
    if not os.path.isdir('./ログ'):
        return

    tree = build_tree('ログ')

    print(header)

    print("<ul>")
    for child in tree["children"]:
        print(render_html(child, add_li=True))
    print("</ul>")

    print(footer)


if __name__ == "__main__":
    main()
