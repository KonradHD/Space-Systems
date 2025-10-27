function enableDropZones(zoneList) {
    zoneList.forEach(vslot => {
        vslot.addEventListener('dragover', e => {
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
        });

        vslot.addEventListener('dragenter', () => {
            if (!vslot.firstElementChild) {
                vslot.classList.add('highlight');
            }
        });

        vslot.addEventListener('dragleave', () => {
            vslot.classList.remove('highlight');
        });

        vslot.addEventListener('drop', e => {
            e.preventDefault();
            vslot.classList.remove('highlight');

            if (vslot.firstElementChild && vslot.firstElementChild !== dragged) return;

            if (dragged) {
                const oldParent = dragged.parentElement;
                oldParent.classList.remove('highlight');
                vslot.appendChild(dragged);
            }
        });
    });
}


function showPopup(popup) {
    popup.classList.add("show");

    setTimeout(() => {
        popup.classList.add("hide");
    }, 2500);

    setTimeout(() => {
        popup.classList.remove("show", "hide");
    }, 3100);
}

// function starting Server-Sent Event
function initSSE() {

    if (source) {
        source.close();
    }

    source = new EventSource("/stream");
    source.addEventListener("message", function (event) {
        const data = JSON.parse(event.data);
        console.log("Ze streama: ", data.state);

        const container = document.querySelector('#rocket-progress');

        container.innerHTML = `
            <pre>${data.rocketstatus}</pre>
            <h1>State: ${data.state}</h1>
            <h4>Sensors:</h4>
            <ul>
                <li>Fuel level: ${data.sensors.fuel_level}%</li>
                <li>Oxidizer level: ${data.sensors.oxidizer_level}%</li>
                <li>Oxidizer pressure: ${data.sensors.oxidizer_pressure} bar</li>
                <li>Altitude: ${data.sensors.altitude} m</li>
                <li>Angle: ${data.sensors.angle}°</li>
            </ul>
            <h4>Servos:</h4>
            <ul>
                <li>Fuel intake: ${data.servos.fuel_intake}</li>
                <li>Oxidizer intake: ${data.servos.oxidizer_intake}</li>
                <li>Fuel main: ${data.servos.fuel_main}</li>
                <li>Oxidizer main: ${data.servos.oxidizer_main}</li>
            </ul>
            <h4>Relays:</h4>
            <ul>
                <li>Oxidizer heater: ${data.relays.oxidizer_heater}</li>
                <li>Igniter: ${data.relays.igniter}</li>
                <li>Parachute: ${data.relays.parachute}</li>
            </ul>
            <h4>Velocity: ${data.velocity} m/s</h4>
            <pre>${data["="]}</pre>
        `;
    });

    source.addEventListener("error", function (event) {
        try {
            const data = JSON.parse(event.data);
            console.log("Error: ", data);
            const container = document.querySelector('#rocket-progress');

            container.innerHTML = `
                <h3>${data.status}</h3>
                <p>Message: ${data.message} </p>
                `;
        } catch (e) {
            console.error("Error parsing SSE data:", e);
        }

        source.close();
        console.warn("SSE connection was closed after an error.");
    });

    source.addEventListener("warning", function (event) {
        try {
            const data = JSON.parse(event.data);
            console.log("Warning: ", data);
            const container = document.querySelector('#rocket-progress');

            container.innerHTML = `
                <h5>${data.status}</h5>
                <p>${data.message} </p>
                `;
        } catch (e) {
            console.error("Error:", e);
        }

        source.close();
        console.warn("SSE connection was closed after a warning.");
    });

    source.addEventListener("success", function (event) {
        const data = JSON.parse(event.data);
        console.log("success");
        const popup = document.querySelector(".landed");
        showPopup(popup);
        try {
            const container = document.querySelector('#rocket-progress');

            container.innerHTML = `
                <h6>${data.status}</h6>
                <p>Message: ${data.message}</p>
                `;
        } catch (e) {
            console.error("Error:", e);
        }
        dataBtn.style.display = "inline-block"
        source.close();
        console.warn("SSE connection was closed after landing.");
    });

    source.addEventListener("fail", function (event) {
        const data = JSON.parse(event.data);
        console.log("fail");
        const popup = document.querySelector(".exploded");
        showPopup(popup);
        try {
            const container = document.querySelector('#rocket-progress');

            container.innerHTML = `
                <h3>${data.status}</h3>
                <p>Message: ${data.message}</p>
                `;
        } catch (e) {
            console.error("Error:", e);
        }
        source.close();
        console.warn("SSE connection was closed after an explosion.");
    });
}

function shuffleButtons() {
    const slots = document.querySelectorAll('.slot');
    const buttons = Array.from(slots).map(slot => slot.querySelector('button'));
    //shuffle
    for (let i = buttons.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [buttons[i], buttons[j]] = [buttons[j], buttons[i]];
    }

    slots.forEach((slot, index) => {
        slot.innerHTML = ''; // Czyści slot
        slot.appendChild(buttons[index]);
    });
}

const buttons = document.querySelectorAll('.answer');
const vslots = document.querySelectorAll('.valid-slot');
const homeSlots = document.querySelectorAll(".slot")
let dragged = null;
let ghost = null;
const hints = document.querySelectorAll('.hints-container p');
const hintBtn = document.getElementById('hint');
let hintIndex = 0;
let source = null
const dataBtn = document.getElementById("dataBtn")


hintBtn.addEventListener('click', () => {

    hints.forEach(h => h.style.display = 'none');

    if (hintIndex < hints.length) {
        hints[hintIndex].style.display = 'block';
        hintIndex++;
    } else {
        hintIndex = 0;
    }
});


dataBtn.addEventListener("click", async () => {
    try {
        const response = await fetch("/api/statistics");
        if (!response.ok) throw new Error("Connection error");

        const data = await response.json();
        console.log(data);

        document.querySelector(".data-display").innerHTML = `
        <h1>Statistics</h1>
        <p><b>Starting oxidizer level: </b> ${data.oxidizer_level_value}%</p>
        <p><b>Oxidizer filling time: </b> ${data.oxidizer_level_time} s</p>
        <p><b>Starting fuel level: </b> ${data.fuel_level_value}%</p>
        <p><b>Fuel filling time: </b> ${data.fuel_level_time} s</p>
        <p><b>Starting oxidizer pressure: </b> ${data.oxidizer_pressure_value} bar</p>
        <p><b>Oxidizer heating time: </b> ${data.oxidizer_pressure_time} s</p>
        <p><b>Max height: </b> ${data.max_height_value} m</p>
        <p><b>Rocket rising time: </b> ${data.max_height_time} s</p>
        <p><b>Falling distance without parachute: </b> ${data.no_parachute_falling_distance} m</p>
        <p><b>Falling time without parachute: </b> ${data.no_parachute_falling_time} s</p>
    `;
    } catch (error) {
        console.error(error);
        document.querySelector(".data-display").innerHTML = `
        <h3>Error</h3>
        <p>Message: Data was not provided.</p>`;
    }
});

shuffleButtons();

// --- DRAG START ---
buttons.forEach(btn => {
    btn.addEventListener('dragstart', e => {
        dragged = btn;
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData('text/plain', btn.textContent);
    });

    btn.addEventListener('drag', e => {
        if (ghost && e.pageX && e.pageY) {
            ghost.style.left = e.pageX + 10 + 'px';
            ghost.style.top = e.pageY + 10 + 'px';
        }
    });

    btn.addEventListener('dragend', () => {
        if (ghost) ghost.remove();
        ghost = null;
        dragged = null;
    });

    const input = btn.querySelector('input');
    if (input) {
        input.addEventListener('mousedown', e => {
            e.stopPropagation(); // żeby przycisk mógł być nadal przeciągany
        });
    }
});


// aktywuje obsługę dla slotów i sekcji początkowej 
enableDropZones(vslots);
enableDropZones(homeSlots)



document.getElementById('check').addEventListener('click', () => {

    initSSE();
    dataBtn.style.display = "none"
    const current = Array.from(vslots).map(vslot => {
        const btn = vslot.querySelector('.answer');

        if (!btn) return {
            name: vslot.textContent.trim(),
            value: 0,
            type: "none"
        };
        const type = btn.dataset.type;
        const input = btn.querySelector('input');
        return {
            name: vslot.textContent.replace(/[\n\t]/g, "").replace(/\s+/g, " ").trim(),
            value: input ? input.value : null,
            type: type
        };
    });

    fetch('/api/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ slots: current })
    })
        .then(response => response.json())
        .then(data => {
            console.log("Backend response", data);
        })
        .catch(error => {
            console.error('Sending error:', error);
        });
});

document.getElementById("reset").addEventListener('click', () => {

    dataBtn.style.display = "none"
    homeSlots.forEach(slot => slot.innerHTML = '');

    buttons.forEach((btn, index) => {
        if (homeSlots[index]) {
            homeSlots[index].appendChild(btn);
        } else {
            console.warn("There is not enough slots for buttons:", btn.textContent);
        }
    });
    shuffleButtons();
    console.log("All buttons came back to the starting slots.");
});
