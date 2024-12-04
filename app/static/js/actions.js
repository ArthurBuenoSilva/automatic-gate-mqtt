const socketio = io();

function openGate() {
    fetch("/open_gate", { method: "POST" }).then(r => {});
}

function closeGate() {
    fetch("/close_gate", { method: "POST" }).then(r => {});
}

function stopGate() {
    fetch("/stop_gate", { method: "POST" }).then(r => {});
}

function getCurrentState() {
    fetch("/get_current_state").then(r => {})
}

socketio.on("update_current_state", (data) => {
    const current_state = document.getElementById("current_state");
    current_state.innerHTML = `Status: ${data}`;
})