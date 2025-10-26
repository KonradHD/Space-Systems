from flask import Flask, request, jsonify, render_template, Response
from command_runner import Runner
import subprocess
from time import sleep
import queue
import json
from flask_sse import sse

app = Flask(__name__)
#app.register_blueprint(command_runner)
#status_queue = queue.Queue()
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")
runner = Runner()


@app.route("/")
def home():
    # cmd", "/c", "start", 
    subprocess.Popen(["python3", "tcp_proxy.py"])
    print("Uruchomienie proxy.")
    sleep(2)
    return render_template("index.html")


@app.route("/api/check", methods=["POST"])
def check():
    runner.reset()
    sleep(2)
    #subprocess.Popen(["python3", "tcp_simulator.py"])
    proc = subprocess.Popen(["python3", "tcp_simulator.py"])
    print("Uruchomienie symulatora")
    data = request.get_json()
    slots = data.get("slots", [])
    sleep(2)
    print("Odebrano: ", slots)
    try:
        statement = runner.run_commands(slots)
        if statement == "Timeout":
            sse.publish({"status" : "Timeout", "message" : "Check, if you registered data or opened appropriate waiting block."}, type="error")
    except ValueError as e:
        sse.publish({"status" : "error", "message" : str(e)}, type="error")
        proc.terminate()
        return jsonify({"status" : "error", "message" : str(e)})
    sleep(2)
    #proc.terminate()
    
    return jsonify({"status" : "ok", "received": slots})



@app.route("/api/oxidizer_data")
def get_oxidizer_data():
    if not runner.oxidizer_level:
        return jsonify({"status": "pending"}), 202
    return jsonify(runner.cmd.oxidizer_level_data)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

    