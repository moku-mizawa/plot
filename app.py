from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        function = request.form['function']
        return redirect(url_for('plot', function=function))
    return render_template('index.html')

@app.route('/plot')
def plot():
    function = request.args.get('function')
    img = io.BytesIO()
    
    x = range(-10, 11)
    y = [eval(function.replace('x', str(i))) for i in x]

    plt.figure()
    plt.plot(x, y)
    plt.title(f'Plot of {function}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template('plot.html', plot_url=plot_url, function=function)

if __name__ == '__main__':
    app.run(debug=True)
