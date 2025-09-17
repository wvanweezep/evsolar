const REFRESH_RATE = 2;

async function pull() {
    // NRGKick
    try {
        const res = await fetch("/api/nrg-state");
        const state = await res.json();
        document.getElementById('nrg-connection-status').textContent = state.connected ? "CONNECTED" : "DISCONNECTED";
        document.getElementById('nrg-connection-status').style.color = state.connected ? "lime" : "red";
        document.getElementById('nrg-last-response').textContent = state.last_response === 0 ? "Now" : `${state.last_response * REFRESH_RATE}s ago`;
        document.getElementById('nrg-status').textContent = state.status;
        document.getElementById('nrg-phase-count').textContent = state.phase_count;
        document.getElementById('nrg-set-current').textContent = state.set_current;
    } catch {}

    // HomeWizard P1
    try {
        const res = await fetch("/api/hw-state");
        const state = await res.json();
        document.getElementById('hw-connection-status').textContent = state.connected ? "CONNECTED" : "DISCONNECTED";
        document.getElementById('hw-connection-status').style.color = state.connected ? "lime" : "red";
        document.getElementById('hw-last-response').textContent = state.last_response === 0 ? "Now" : `${state.last_response * REFRESH_RATE}s ago`;
        document.getElementById('hw-current-l1').textContent = state.l1_a;
        document.getElementById('hw-current-l2').textContent = state.l2_a;
        document.getElementById('hw-current-l3').textContent = state.l3_a;
    } catch {}
}

pull();
setInterval(pull, REFRESH_RATE * 1000);
