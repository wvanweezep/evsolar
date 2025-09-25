import logging
import os, threading, time

from flask import Flask, jsonify, render_template, request

from commons.debug import Debug
from services.homewizard import HomeWizard, HWState
from services.nrgkick import NRGKick, NRGState
from services.solarcharge import SolarCharge

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

hw = HomeWizard(os.getenv("HOMEWIZARD_BASE_URL"))
nrg = NRGKick(os.getenv("NRGKICK_BASE_URL"))
sc = SolarCharge(nrg)

nrg_state = NRGState()
hw_state = HWState()
solar_charging = True


######################################## Background Poller ########################################
def poll_loop() -> None:
    while True:
        try:
            control = nrg.get_control()
            values = nrg.get_values()
            nrg_state.connected = True
            nrg_state.last_response = 0
            nrg_state.status = values.get("general", {}).get("status", "UNKNOWN")
            nrg_state.phase_count = control.get("phase_count", None)
            nrg_state.set_current = control.get("current_set", None)
        except:
            nrg_state.connected = False
            nrg_state.last_response += 1

        try:
            data = hw.get_data()
            hw_state.connected = True
            hw_state.last_response = 0
            hw_state.l1_a = data.get("active_current_l1_a", None)
            hw_state.l2_a = data.get("active_current_l2_a", None)
            hw_state.l3_a = data.get("active_current_l3_a", None)
        except:
            hw_state.connected = False
            hw_state.last_response += 1

        if solar_charging:
            total_amps: float = hw_state.l1_a + hw_state.l2_a + hw_state.l3_a
            sc.update(total_amps, nrg_state.set_current)

        time.sleep(2)


######################################## Routes ########################################
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/nrg-state")
def api_nrg_state():
    return jsonify({
        "connected": nrg_state.connected,
        "last_response": nrg_state.last_response,
        "status": nrg_state.status,
        "phase_count": nrg_state.phase_count,
        "set_current": nrg_state.set_current
    })

@app.route("/api/hw-state")
def api_hw_state():
    return jsonify({
        "connected": hw_state.connected,
        "last_response": hw_state.last_response,
        "l1_a": hw_state.l1_a,
        "l2_a": hw_state.l2_a,
        "l3_a": hw_state.l3_a
    })

@app.route('/submit', methods=['POST'])
def cp_manual_submit():
    data = request.get_json()
    nrg.pause(bool(data.get('charging')))
    nrg.set_phases(int(data.get('phase_count')))
    nrg.set_current(float(data.get('set_current')))
    return jsonify({"status": "ok"})



if __name__ == "__main__":
    thread = threading.Thread(target=poll_loop, daemon=True)
    thread.start()
    Debug.log("[Main] Starting Application...", 1)
    app.run(host="0.0.0.0", port=8000)
