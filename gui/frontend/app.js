async function fetchJSON(url) {
    const r = await fetch(url);
    return r.json();
}

async function refresh() {
    const status = await fetchJSON("/api/status");
    const progress = await fetchJSON("/api/progress");
    const phases = await fetchJSON("/api/phases");
    const log = await fetchJSON("/api/log");

    document.getElementById("currentStage").textContent = status.stage;
    document.getElementById("progressFill").style.width = progress.percent + "%";

    const p = document.getElementById("phases");
    p.innerHTML = "";
    for (const k in phases) {
        p.innerHTML += k + ": " + phases[k] + "%<br>";
    }

    document.getElementById("logOutput").textContent = log.lines.join("\n");
}

setInterval(refresh, 1000);
