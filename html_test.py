from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/try.html')
def serve_try_html():
    return send_from_directory('C:/Users/Mahua Mukhopadhyay/Desktop/Intern', 'try.html')

if __name__ == '__main__':
    app.run(debug=True)
