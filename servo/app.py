from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/control", methods=["POST"])
def control():
    slider1 = request.form["slider1"]
    slider2 = request.form["slider2"]

    # Send the servo angles to the Pico
    with open("/dev/ttyACM0", "w") as pico:
        pico.write(f"{slider1},{slider2}\n")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)