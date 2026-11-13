from flask import Flask, jsonify, render_template_string
import psutil
import platform
import os
import time
from datetime import datetime

app = Flask(__name__)

start_time = time.time()

previous_net = psutil.net_io_counters()
previous_time = time.time()


HTML = """
<!DOCTYPE html>
<html>
<head>

<title>System Health Monitoring</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<meta http-equiv="refresh" content="">

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: #f1f5f9;
    color: #1e293b;
}

header {
    background: #172554;
    color: white;
    padding: 25px;
    text-align: center;
}

header h1 {
    margin-bottom: 8px;
}

.container {
    padding: 30px;
    max-width: 1300px;
    margin: auto;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-top: 25px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.card h3 {
    color: #64748b;
    margin-bottom: 15px;
}

.value {
    font-size: 30px;
    font-weight: bold;
    color: #2563eb;
}

.section {
    background: white;
    margin-top: 25px;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    overflow-x: auto;
}

.section h2 {
    margin-bottom: 20px;
}

.progress {
    background: #e2e8f0;
    height: 10px;
    border-radius: 10px;
    margin-top: 12px;
    overflow: hidden;
}

.bar {
    height: 10px;
    background: #2563eb;
    border-radius: 10px;
    transition: width 0.4s;
}

.status {
    font-weight: bold;
    color: #16a34a;
}

.warning {
    color: #dc2626;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 550px;
}

th, td {
    padding: 14px;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
}

th {
    background: #eff6ff;
}

button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 12px 22px;
    border-radius: 6px;
    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}

footer {
    text-align: center;
    padding: 25px;
    color: #64748b;
}

@media(max-width:600px) {
    .container {
        padding: 15px;
    }

    .value {
        font-size: 25px;
    }
}

</style>

</head>

<body>

<header>

<h1>System Health Monitoring Service</h1>

<p>Professional Real-Time System Monitoring Dashboard</p>

</header>

<div class="container">

<div class="cards">

<div class="card">

<h3>CPU Usage</h3>

<div class="value" id="cpu">--%</div>

<div class="progress">
<div class="bar" id="cpuBar"></div>
</div>

</div>


<div class="card">

<h3>RAM Usage</h3>

<div class="value" id="ram">--%</div>

<div class="progress">
<div class="bar" id="ramBar"></div>
</div>

<p id="ramDetails"></p>

</div>


<div class="card">

<h3>Disk Usage</h3>

<div class="value" id="disk">--%</div>

<div class="progress">
<div class="bar" id="diskBar"></div>
</div>

<p id="diskDetails"></p>

</div>


<div class="card">

<h3>System Health</h3>

<div class="value status" id="health">Loading</div>

<p id="healthMessage"></p>

</div>


<div class="card">

<h3>Download Speed</h3>

<div class="value" id="download">0 KB/s</div>

</div>


<div class="card">

<h3>Upload Speed</h3>

<div class="value" id="upload">0 KB/s</div>

</div>

</div>


<div class="section">

<h2>System Information</h2>

<table>

<tr>
<th>Information</th>
<th>Details</th>
</tr>

<tr>
<td>Operating System</td>
<td id="os">Loading</td>
</tr>

<tr>
<td>Processor</td>
<td id="processor">Loading</td>
</tr>

<tr>
<td>CPU Cores</td>
<td id="cores">Loading</td>
</tr>

<tr>
<td>Total RAM</td>
<td id="totalRam">Loading</td>
</tr>

<tr>
<td>System Uptime</td>
<td id="uptime">Loading</td>
</tr>

<tr>
<td>Last Updated</td>
<td id="updated">Loading</td>
</tr>

</table>

</div>


<div class="section">

<h2>Running Processes</h2>

<table>

<thead>

<tr>
<th>Process ID</th>
<th>Process Name</th>
<th>CPU Usage</th>
<th>Memory Usage</th>
</tr>

</thead>

<tbody id="processes">

<tr>
<td colspan="4">Loading processes...</td>
</tr>

</tbody>

</table>

</div>


<div class="section">

<h2>Monitoring Controls</h2>

<p id="refreshStatus">
Automatic monitoring is active.
</p>

<br>

<button onclick="loadData()">
Refresh Now
</button>

</div>

</div>


<footer>

<p>System Health Monitoring Service</p>
<p>Powered by Python, Flask and Psutil</p>

</footer>


<script>

async function loadData() {

    try {

        const response = await fetch('/api/metrics');

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        document.getElementById("cpu").innerText =
            data.cpu + "%";

        document.getElementById("ram").innerText =
            data.ram + "%";

        document.getElementById("disk").innerText =
            data.disk + "%";


        document.getElementById("cpuBar").style.width =
            data.cpu + "%";

        document.getElementById("ramBar").style.width =
            data.ram + "%";

        document.getElementById("diskBar").style.width =
            data.disk + "%";


        document.getElementById("ramDetails").innerText =
            data.ram_used + " GB used / " +
            data.ram_total + " GB total";


        document.getElementById("diskDetails").innerText =
            data.disk_used + " GB used / " +
            data.disk_total + " GB total";


        document.getElementById("health").innerText =
            data.health;


        document.getElementById("health").className =
            data.health === "Healthy"
            ? "value status"
            : "value warning";


        document.getElementById("healthMessage").innerText =
            data.message;


        document.getElementById("download").innerText =
            data.download + " KB/s";

        document.getElementById("upload").innerText =
            data.upload + " KB/s";


        document.getElementById("os").innerText =
            data.os;

        document.getElementById("processor").innerText =
            data.processor;

        document.getElementById("cores").innerText =
            data.cores;

        document.getElementById("totalRam").innerText =
            data.ram_total + " GB";

        document.getElementById("uptime").innerText =
            data.uptime;

        document.getElementById("updated").innerText =
            data.updated;


        let processHTML = "";

        data.processes.forEach(function(p) {

            processHTML += `
            <tr>
                <td>${p.pid}</td>
                <td>${p.name}</td>
                <td>${p.cpu}%</td>
                <td>${p.memory}%</td>
            </tr>
            `;

        });

        document.getElementById("processes").innerHTML =
            processHTML;

        document.getElementById("refreshStatus").innerText =
            "Monitoring active. Last updated: " + data.updated;

    }

    catch(error) {

        document.getElementById("refreshStatus").innerText =
            "Unable to connect to monitoring server.";

        console.error(error);

    }

}


loadData();

setInterval(loadData, 5000);

</script>

</body>
</html>
"""


def get_system_data():

    global previous_net, previous_time

    cpu = psutil.cpu_percent(interval=0.2)

    memory = psutil.virtual_memory()

    disk = psutil.disk_usage(os.path.abspath(os.sep))

    current_net = psutil.net_io_counters()

    current_time = time.time()

    elapsed = max(current_time - previous_time, 0.001)

    download = (
        current_net.bytes_recv - previous_net.bytes_recv
    ) / elapsed / 1024

    upload = (
        current_net.bytes_sent - previous_net.bytes_sent
    ) / elapsed / 1024

    previous_net = current_net
    previous_time = current_time

    if cpu >= 90 or memory.percent >= 90 or disk.percent >= 95:

        health = "Critical"
        message = "High system resource usage detected."

    elif cpu >= 80 or memory.percent >= 80 or disk.percent >= 90:

        health = "Warning"
        message = "System resources are running high."

    else:

        health = "Healthy"
        message = "System is operating within normal thresholds."


    uptime_seconds = int(time.time() - start_time)

    hours, remainder = divmod(uptime_seconds, 3600)

    minutes, seconds = divmod(remainder, 60)

    uptime = f"{hours}h {minutes}m {seconds}s"


    processes = []

    for process in psutil.process_iter(
        ['pid', 'name', 'memory_percent']
    ):

        try:

            info = process.info

            processes.append({

                "pid": info['pid'],

                "name": info['name'] or "Unknown",

                "cpu": round(process.cpu_percent(None), 2),

                "memory": round(
                    info['memory_percent'] or 0, 2
                )

            })

        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):

            continue


    processes.sort(
        key=lambda x: x['memory'],
        reverse=True
    )


    return {

        "cpu": round(cpu, 2),

        "ram": round(memory.percent, 2),

        "ram_used": round(memory.used / (1024 ** 3), 2),

        "ram_total": round(memory.total / (1024 ** 3), 2),

        "disk": round(disk.percent, 2),

        "disk_used": round(disk.used / (1024 ** 3), 2),

        "disk_total": round(disk.total / (1024 ** 3), 2),

        "download": round(max(download, 0), 2),

        "upload": round(max(upload, 0), 2),

        "health": health,

        "message": message,

        "os": platform.system() + " " + platform.release(),

        "processor": platform.processor() or "Not Available",

        "cores": psutil.cpu_count(logical=True),

        "uptime": uptime,

        "updated": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),

        "processes": processes[:10]

    }


@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/api/metrics")
def metrics():

    return jsonify(get_system_data())


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )