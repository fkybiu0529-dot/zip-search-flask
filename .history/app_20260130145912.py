from flask import Flask, request, render_template
import csv
import os

app = Flask(__name__)

# CSVファイルを読み込んで郵便番号と住所のリストを作成
def load_zip_data():
    data = []
    # app.py と同じフォルダにある CSV を絶対パスで指定
    csv_path = os.path.join(os.path.dirname(__file__), "KEN_ALL.CSV")
    with open(csv_path, encoding="shift_jis") as f:
        reader = csv.reader(f)
        for row in reader:
            zipcode = row[1]
            
            prefecture = row[6]           # 都道府県
            city = row[7]                 # 市区町村
            town = row[8]                 # 町域
            data.append({
                "zipcode": zipcode,
                "address": prefecture + city + town
            })
    return data

# 読み込んだデータをグローバル変数として保持
zip_data = load_zip_data()

# 郵便番号から住所を検索する関数
def search_by_zip(zipcode):
    for row in zip_data:
        if row["zipcode"] == zipcode:
            return row["address"]
    return "該当する住所が見つかりませんでした"

# 住所から郵便番号を検索する関数
def search_by_address(keyword):
    results = []
    for row in zip_data:
        if keyword in row["address"]:
            results.append(f"{row['zipcode']}：{row['address']}")
    results = "<br>".join(results)
    return results or "該当する郵便番号が見つかりませんでした"

# トップページ（index.htmlを表示）
@app.route("/")
def home():
    return render_template("index.html")

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