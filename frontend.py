from flask import Flask, request, render_template_string, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/')
def index():
    html = '''
    <html>
        <body>
            <h2>Введите данные для отправки на сервер:</h2>
            <form action="/send" method="POST">
                <input type="text" name="userInput" placeholder="Введите текст">
                <button type="submit">Отправить</button>
            </form>
        </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/send', methods=['POST'])
def send():
    user_input = request.form['userInput']

    if not user_input.strip():
        return redirect(url_for('no_data'))

    response = requests.post('http://127.0.0.1:5001/save', json={'data': user_input})

    return render_template_string(f'''
    <html>
        <body>
            <h2>Данные отправлены на сервер: {user_input}</h2>
            <p>Ответ сервера: {response.text}</p>
            <a href="/">Вернуться на главную страницу</a>
        </body>
    </html>
    ''')


@app.route('/no_data')
def no_data():
    html = '''
    <html>
        <body>
            <h2">Нет данных для отправки. Пожалуйста, введите текст.</h2>
            <a href="/">Вернуться на главную страницу</a>
        </body>
    </html>
    '''
    return render_template_string(html)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
