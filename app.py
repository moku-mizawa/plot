from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

# Use the Agg backend for Matplotlib
plt.switch_backend('Agg')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        functions = request.form.getlist('functions')
        smooth = request.form.get('smooth', 'off') == 'on'
        grid = request.form.get('grid', 'on') == 'on'
        return redirect(url_for('plot', functions=";".join(functions), smooth=smooth, grid=grid))
    return render_template('index.html')

@app.route('/plot')
def plot():
    functions = request.args.get('functions').split(';')
    smooth = request.args.get('smooth') == 'True'
    grid = request.args.get('grid') == 'True'
    
    img = io.BytesIO()
    x = np.linspace(-10, 10, 400)

    plt.figure()
    
    for function in functions:
        try:
            # Use eval with numpy namespace for safe function evaluation
            y = np.array([eval(function, {"__builtins__": None, "np": np, "x": i}) for i in x])
            if smooth:
                y = np.convolve(y, np.ones(10)/10, mode='same')  # simple smoothing with a window size of 10
            plt.plot(x, y, label=function)
        except Exception as e:
            return f"Error in function evaluation: {e}", 400

    plt.title('Plot of Functions')
    plt.xlabel('x')
    plt.ylabel('y')
    if grid:
        plt.grid(True)
    else:
        plt.grid(False)
    plt.legend()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template('plot.html', plot_url=plot_url, functions=functions, smooth=smooth, grid=grid)

if __name__ == '__main__':
    app.run(debug=True)

