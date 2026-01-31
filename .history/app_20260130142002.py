from flask import Flask, request, render_template
import csv

app = Flask(__name__)

# CSV読み込み
def load_zip_data():
    data = []
    with open("KEN_ALL.CSV", encoding="shift_jis") as f:
        reader = csv.reader(f)
        for row in reader:
            zipcode = row[2]
            prefecture = row[6]
            city = row[7]
            town = row[8]
            data.append({
                "zipcode": zipcode,
                "address": prefecture + city + town
            })
    return data

zip_data = load_zip_data()

# 郵便番号 → 住所検索
def search_by_zip(zipcode):
    for row in zip_data:
        if row["zipcode"] == zipcode:
            return row["address"]
    return "該当する住所が見つかりませんでした"

# トップページ
@app.route("/")
def home():
    return render_template("index.html")

# 郵便番号検索ルート
@app.route("/zip")
def zip_to_address():
    zipcode = request.args.get("zipcode")
    result = search_by_zip(zipcode)
    return f"郵便番号 {zipcode} の住所は：{result}"

if __name__ == "__main__":
    app.run(debug=True)