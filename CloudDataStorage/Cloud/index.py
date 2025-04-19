

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import logout_user, login_user, current_user
import cloudinary.uploader
import dao
from CloudDataStorage.Cloud import app, login_manager


@app.route("/")
def home():
   return render_template('index.html')  # Hiển thị trang chủ

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated :
        return redirect("/")
    err_msg = None
    if request.method.__eq__('POST'):
        email = request.form['email']
        password = request.form.get('password')
        user = dao.auth_user(email=email, password=password)
        if user :
            login_user(user)
            next_page = request.args.get("next", "/")
            return redirect(next_page)
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)

@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        if password.__eq__(confirm):
            # Kiểm tra email đã tồn tại
            if dao.check_email_exists(email):
                err_msg = "Email đã được đăng ký!"
            else:
                name = request.form.get('name')
                dao.add_user(name=name, email=email, password=password)
                return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp!"
    return render_template('register.html', err_msg=err_msg)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')  # Quay về trang chủ sau khi đăng xuất

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
