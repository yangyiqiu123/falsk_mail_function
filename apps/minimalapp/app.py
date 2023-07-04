from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

# 繼續定義其他函式或類


@app.route("/")
def index():
    # url_for("static", filename="static")

    return "Hello"


@app.route("/name/<name>")
def show_name(name):
    # 変数をテンプレートエンジンに渡す
    return render_template("index.html", name=name)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    # 當使用者提交表單時，使用POST方法將表單數據發送給伺服器。
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("必須填使用者名稱")
            is_valid = False

        if not email:
            flash("必須填電子郵件")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("輸入正確的電子郵件")
            is_valid = False

        if not description:
            flash("必須填寫諮詢內容")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        flash("諮詢內容已傳送")

        # 完成表單處理後，伺服器會使用重定向將使用者重定向到另一個頁面（通常是GET請求的目標頁面），而不是直接返回回應。
        return redirect(url_for("contact_complete"))
    # 最終，客戶端收到重定向的回應後，會發起一個GET請求獲取重定向目標頁面的內容。
    return render_template("contact_complete.html")
