const REFRESH_RATE = 2;

document.addEventListener("DOMContentLoaded", () => {
    const manual_form = document.getElementById("cp-manual-form");
    manual_form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const charging = document.getElementById("cp-charging").checked;
        const phaseCount = parseInt(document.getElementById("cp-phase-count").value, 10);
        const setCurrent = parseFloat(document.getElementById("cp-set-current").value);

        await fetch("/submit", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                charging: charging,
                phase_count: phaseCount,
                set_current: setCurrent
            })
        });
    });
});

async function pull() {
    await nrg_update()
    await hw_update();
}

async function nrg_update() {
    try {
        const res = await fetch("/api/nrg-state");
        const state = await res.json();
        document.getElementById('nrg-connection-status').textContent = state.connected ? "CONNECTED" : "DISCONNECTED";
        document.getElementById('nrg-connection-status').style.color = state.connected ? "lime" : "red";
        document.getElementById('nrg-last-response').textContent = state.last_response === 0 ? "Now" : `${state.last_response * REFRESH_RATE}s ago`;
        document.getElementById('nrg-status').textContent = state.status;
        document.getElementById('nrg-phase-count').textContent = state.phase_count;
        document.getElementById('nrg-set-current').textContent = state.set_current;
        return state;
    } catch {
    }
}

async function hw_update() {
    try {
        const res = await fetch("/api/hw-state");
        const state = await res.json();
        document.getElementById('hw-connection-status').textContent = state.connected ? "CONNECTED" : "DISCONNECTED";
        document.getElementById('hw-connection-status').style.color = state.connected ? "lime" : "red";
        document.getElementById('hw-last-response').textContent = state.last_response === 0 ? "Now" : `${state.last_response * REFRESH_RATE}s ago`;
        document.getElementById('hw-current-l1').textContent = state.l1_a;
        document.getElementById('hw-current-l2').textContent = state.l2_a;
        document.getElementById('hw-current-l3').textContent = state.l3_a;
        return state;
    } catch {
    }
}

async function cp_update() {
    const nrg_state = await nrg_update()
    document.getElementById('cp-charging').checked = nrg_state.status === "CHARGING";
    document.getElementById('cp-phase-count').value = nrg_state.phase_count;
    document.getElementById('cp-set-current').value = nrg_state.set_current;
}

cp_update()
pull();
setInterval(pull, REFRESH_RATE * 1000);
