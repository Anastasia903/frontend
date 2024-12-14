from flask import Flask, request, render_template_string, redirect, url_for
import requests
import os

app = Flask(__name__)

# Указываем абсолютный путь к файлу data.txt
FILE_PATH = 'D:/Учеба/DO/lab/backend/data.txt'  # Замените на ваш абсолютный путь

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
            <br>
            <a href="/view">Посмотреть данные из файла</a>
        </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/send', methods=['POST'])
def send():
    user_input = request.form['userInput']

    if not user_input.strip():
        return redirect(url_for('no_data'))

    # Отправляем данные на второй сервер
    response = requests.post('http://backend:5001/save', json={'data': user_input})
    #response = requests.post('http://127.0.0.1:5001/save', json={'data': user_input})


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


@app.route('/view')
def view_data():
    try:
        # Проверяем, существует ли файл
        if not os.path.exists(FILE_PATH):
            return render_template_string('''
            <html>
                <body>
                    <h2>Файл data.txt не найден.</h2>
                    <a href="/">Вернуться на главную страницу</a>
                </body>
            </html>
            ''')

        # Читаем данные из файла
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            data = file.read()

        # Отображаем данные на странице
        return render_template_string(f'''
        <html>
            <body>
                <h2>Данные из файла data.txt:</h2>
                <pre>{data}</pre>
                <br>
                <a href="/">Вернуться на главную страницу</a>
            </body>
        </html>
        ''')
    except Exception as e:
        return render_template_string(f'''
        <html>
            <body>
                <h2>Ошибка при чтении файла: {str(e)}</h2>
                <a href="/">Вернуться на главную страницу</a>
            </body>
        </html>
        ''')


if __name__ == '__main__':
    print(f"Сервер запущен. Файл будет создан в: {FILE_PATH}")
    app.run(port=5000, debug=True)