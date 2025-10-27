from flask import Flask, request, jsonify, render_template
from command_runner import Runner
import subprocess
from time import sleep
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost" # server redis
app.register_blueprint(sse, url_prefix="/stream")
runner = Runner()
proc = None  # globalny wskaźnik na proces


@app.route("/")
def home(): 
    subprocess.Popen(["python3", "tcp_proxy.py"])
    print("Uruchomienie proxy.")
    sleep(1)
    return render_template("index.html")


@app.route("/api/check", methods=["POST"])
def check():
    global proc
    if proc is not None:
        proc.terminate()
        sleep(2)
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            print("Proces was not ended.")
            proc.kill()
    proc = subprocess.Popen(["python3", "tcp_simulator.py"])
    print("Uruchomienie symulatora")
    sleep(1)
    runner.reset()

    data = request.get_json()
    slots = data.get("slots", [])

    try:
        landing = runner.run_commands(slots)
        if landing == 1:
            sse.publish({"status" : "Timeout", "message" : "Check, if you registered data or opened appropriate waiting block."}, type="error")
        if landing == 2:
            sse.publish({"status" : "Interrupted", "message" : "Check, if you are waiting till the rocket will land."}, type="warning")
    except ValueError as e:
        sse.publish({"status" : "error", "message" : str(e)}, type="error")
        proc.terminate()
        return jsonify({"status" : "error", "message" : str(e)})
    
    return jsonify({"status" : "ok"})



@app.route("/api/statistics")
def get_statistics():
    return jsonify(runner.get_data())


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

    