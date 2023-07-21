import logging
import os

from email_validator import EmailNotValidError, validate_email

# from flask import response  # 刪除 cookie 值;
from flask import make_response  # 刪除 cookie 值; 設定 coolie 值;
from flask import render_template  # 刪除 cookie 值; 設定 coolie 值;
from flask import request  # 設定 cookie 值;
from flask import Flask, current_app, flash, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

# veriable

debug_tool_on = True

# 取得 cookie 值
# username = request.cookies.get("username")


# app
# def create_app():
#     app = Flask(__name__)
#     from apps.crud import views as crud_views

#     app.register_blueprint(crud_views.crud, url_prefix="/crud")
#     return app
app = Flask(__name__)


app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

app.logger.setLevel(logging.DEBUG)

# debug 工具
if debug_tool_on:
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    toolbar = DebugToolbarExtension(app)

app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)


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
    # return render_template("contact.html")

    # 從 contact.html 取得 Response 物件(response)
    # make_response(render_template("contact.html"))這段程式碼本身並不能直接取得在 contact.html 中輸入的變數。
    # make_response(render_template("contact.html")) 的作用是將渲染後的 contact.html 模板轉換為一個 Response 物件，並返回給客戶端作為 HTTP 回應的一部分。
    response = make_response(render_template("contact.html"))

    # 設定 cookie
    response.set_cookie("flaskbook key", "flaskbook value")

    # 設定 session
    session["username"] = "young"

    # 回應 Response 物件
    return response

# 
# 當用戶提交表單後，如果刷新頁面，可能會導致表單數據再次提交。這是因為瀏覽器在提交表單後會保留最後提交的表單數據，並在用戶刷新頁面時重新發送相同的 POST 請求。
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

        send_email(
            email,
            "感謝來信讚美邱暘壹 帥吧",
            "contact_mail",
            username=username,
            description=description,
        )
        # 完成表單處理後，伺服器會使用重定向將使用者重定向到另一個頁面（通常是GET請求的目標頁面），而不是直接返回回應。
        return redirect(url_for("contact_complete"))
    # 最終，客戶端收到重定向的回應後，會發起一個GET請求獲取重定向目標頁面的內容。
    return render_template("contact_complete.html")


# \ **kwargs表示接受任意数量的关键字参数。在函数调用时，您可以传递额外的关键字参数，它们将被打包成一个字典并传递给函数。
def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
