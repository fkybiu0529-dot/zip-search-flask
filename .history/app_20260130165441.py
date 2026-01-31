from flask import Flask, request, render_template
import csv
import os

app = Flask(__name__)

# CSVファイルを読み込んで郵便番号と住所のリストを作成
def load_zip_data():
    data = []
    csv_path = os.path.join(os.path.dirname(__file__), "KEN_ALL.CSV")
    with open(csv_path, encoding="utf-8") as f:  # ← 文字コードをutf-8に
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 7:
                continue
            zipcode = str(row[1]).strip()
            prefecture = row[4].strip()
            city = row[5].strip()
            town = row[6].strip()
            data.append({
                "zipcode": zipcode,
                "address": prefecture + city + town
            })
    return data

# 読み込んだデータをグローバル変数として保持
zip_data = load_zip_data()

# 郵便番号から住所を検索する関数
def search_by_zip(zipcode):
    # 入力された郵便番号を整形（ハイフンや空白を除去）
    if zipcode is None:
        return "郵便番号が指定されていません"
    zipcode = zipcode.replace("-", "").strip()

    for row in zip_data:
        if row["zipcode"] == zipcode:
            return row["address"]
    return "該当する住所が見つかりませんでした"

# 住所から郵便番号を検索する関数
def search_by_address(keyword):
    if not keyword:
        return "住所キーワードが指定されていません"

    results = []
    for row in zip_data:
        if keyword in row["address"]:
            results.append(f"{row['zipcode']}：{row['address']}")
    results = "<br>".join(results)
    return results or "該当する郵便番号が見つかりませんでした"

# トップページ＋結果表示を1つにまとめたルート  ←★ ここに書き換える
@app.route("/")
def home():
    zipcode = request.args.get("zipcode")
    keyword = request.args.get("keyword")

    zip_result = None
    address_result = None

    if zipcode:
        zip_result = search_by_zip(zipcode)

    if keyword:
        address_result = search_by_address(keyword)

    return render_template(
        "index.html",
        zip_result=zip_result,
        address_result=address_result
    )

# 郵便番号検索ルート（例：/zip?zipcode=9012301）
@app.route("/zip")
def zip_to_address():
    zipcode = request.args.get("zipcode")
    result = search_by_zip(zipcode)
    return f"郵便番号 {zipcode} の住所は：{result}"

# 住所検索ルート（例：/address?keyword=今帰仁村）
@app.route("/address")
def address_to_zip():
    keyword = request.args.get("keyword")
    result = search_by_address(keyword)
    return f"住所「{keyword}」に該当する郵便番号：<br>{result}"

# アプリ起動
if __name__ == "__main__":
    app.run(debug=True)