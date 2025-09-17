import os, threading, time

from flask import Flask, jsonify

from commons.debug import Debug
from services.homewizard import HomeWizard
from services.nrgkick import NRGKick

app = Flask(__name__)

hw = HomeWizard(os.getenv("HOMEWIZARD_BASE_URL"))
nrg = NRGKick(os.getenv("NRGKICK_BASE_URL"))


######################################## Background Poller ########################################
def poll_loop() -> None:
    while True:
        ...
        time.sleep(5)


######################################## Routes ########################################
@app.route("/")
def index():
    return jsonify("Work in progress...")



if __name__ == "__main__":
    thread = threading.Thread(target=poll_loop, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=8000)