from flask import Flask, request, render_template
import csv

app = Flask(__name__)

# CSVファイルを読み込んで郵便番号と住所のリストを作成
def load_zip_data():
    data = []
    with open("KEN_ALL.CSV", encoding="shift_jis") as f:
        reader = csv.reader(f)
        for row in reader:
            zipcode = row[2]               # 郵便番号
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

# 住所 → 郵便番号検索
def search_by_address(keyword):
    results = []
    for row in zip_data:
        if keyword in row["address"]:
            results.append(f"{row['zipcode']} : {row['address']}")
    if results:
        return "<br>".join(results)
    else:
        return "該当する郵便番号が見つかりませんでした"

# 住所検索ルート（例：/address?keyword=今帰仁村）
@app.route("/address")
def address_to_zip():
    keyword = request.args.get("keyword")
    result = search_by_address(keyword)
    return f"住所「{keyword}」に該当する郵便番号：<br>{result}"

# アプリ起動
if __name__ == "__main__":
    app.run(debug=True)