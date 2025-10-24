from flask import Flask, request, jsonify, render_template
from command_runner import run_commands
import subprocess
from time import sleep

app = Flask(__name__)


@app.route("/")
def home():
    subprocess.run(["python", "tcp_proxy.py"])
    sleep(2)
    subprocess.run(["python", "tcp_simulator.py"])
    return render_template("index.html")

@app.route("/api/check", methods=["POST"])
def check():
    data = request.get_json()
    slots = data.get("slots", [])
    run_commands(slots)
    print("Oebrano: ", slots)
    return jsonify({"status" : "ok", "received": slots})

if __name__ == "__main__":
    app.run(debug=True)