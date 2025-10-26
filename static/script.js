let source = null

function initSSE() {

    if (source) {
        source.close();
    }

    source = new EventSource("/stream");
    source.addEventListener("message", function (event) {
        const data = JSON.parse(event.data);
        console.log("Ze streama: ", data.state);

        // funkcja tworząca HTML z danych
        const container = document.querySelector('#rocket-progress');

        // tworzymy listę dla sensorów
        const sensorsHtml = Object.entries(data.sensors)
            .map(([key, value]) => `<li>${key}: ${value}</li>`)
            .join('');

        // lista dla serwomechanizmów
        const servosHtml = Object.entries(data.servos)
            .map(([key, value]) => `<li>${key}: ${value}</li>`)
            .join('');

        // lista dla przekaźników
        const relaysHtml = Object.entries(data.relays)
            .map(([key, value]) => `<li>${key}: ${value}</li>`)
            .join('');

        // wstawiamy wszystko do diva
        container.innerHTML = `
            <pre>${data.rocketstatus}</pre>
            <h1>State: ${data.state}</h1>
            <h4>Sensors:</h4>
            <ul>${sensorsHtml}</ul>
            <h4>Servos:</h4>
            <ul>${servosHtml}</ul>
            <h4>Relays:</h4>
            <ul>${relaysHtml}</ul>
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
        console.warn("Połączenie SSE zostało zamknięte po błędzie.");
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
        console.warn("Połączenie SSE zostało zamknięte po błędzie.");
    })

}

const buttons = document.querySelectorAll('.answer');
const vslots = document.querySelectorAll('.valid-slot');
const homeSlots = document.querySelectorAll(".slot")
let dragged = null;
let ghost = null;


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

    // --- Zapobiegamy blokowaniu drag przez input ---
    const input = btn.querySelector('input');
    if (input) {
        input.addEventListener('mousedown', e => {
            e.stopPropagation(); // żeby przycisk mógł być nadal przeciągany
        });
    }
});


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

            // jeśli slot ma już przycisk i to nie ten sam — blokuj
            if (vslot.firstElementChild && vslot.firstElementChild !== dragged) return;

            // przenieś przycisk do slotu
            if (dragged) {
                const oldParent = dragged.parentElement;
                oldParent.classList.remove('highlight');
                vslot.appendChild(dragged);
            }
        });
    });
}


// Aktywujemy obsługę dla slotów i początkowej sekcji
enableDropZones(vslots);
enableDropZones(homeSlots)


// --- SPRAWDZENIE UŁOŻENIA ---
document.getElementById('check').addEventListener('click', () => {

    initSSE();

    // Pobieramy tekst + wartość input (jeśli jest)
    const current = Array.from(vslots).map(vslot => {
        const btn = vslot.querySelector('.answer');
        if (!btn) return {
            name: vslot.textContent.trim(),
            value: 0
        };
        const input = btn.querySelector('input');
        return {
            name: vslot.textContent.replace(/[\n\t]/g, "").trim(),
            value: input ? input.value : null
        };
    });

    // wysyłka do backendu
    fetch('/api/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ slots: current })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Odpowiedź z backendu:', data);
        })
        .catch(error => {
            console.error('Błąd przy wysyłaniu:', error);
        });
});



/* fetch("/api/oxidizer_data").then(response => response.json())
                   .then(data => {
                    console.log("Czas: ", data["time"]);
                    document.getElementById("rocket-progress").innerHTML = `
                    <p> ${data.time}</p>
                    `
                   }); */

async function pollOxidizerData(url) {
    while (true) {
        try {
            const res = await fetch(url);
            const data = await res.json();

            if (data.status !== "pending") {
                console.log("Gotowe dane:", data);
                document.getElementById("rocket-progress").innerHTML = `
                    <p> ${data.time}</p>
                    `;
                break;
            }
        } catch (err) {
            console.error("Błąd fetch:", err);
        }
        await new Promise(resolve => setTimeout(resolve, 4000)); // czeka 4 sekundy
    }
}

// pollOxidizerData("/api/oxidizer_data");


// const source = new EventSource("/stream");
// source.addEventListener("message", function (event) {
//     const data = JSON.parse(event.data);
//     console.log("Ze streama: ", data.state);

//     // funkcja tworząca HTML z danych
//     const container = document.querySelector('#rocket-progress');

//     // tworzymy listę dla sensorów
//     const sensorsHtml = Object.entries(data.sensors)
//         .map(([key, value]) => `<li>${key}: ${value}</li>`)
//         .join('');

//     // lista dla serwomechanizmów
//     const servosHtml = Object.entries(data.servos)
//         .map(([key, value]) => `<li>${key}: ${value}</li>`)
//         .join('');

//     // lista dla przekaźników
//     const relaysHtml = Object.entries(data.relays)
//         .map(([key, value]) => `<li>${key}: ${value}</li>`)
//         .join('');

//     // wstawiamy wszystko do diva
//     container.innerHTML = `
//         <pre>${data.rocketstatus}</pre>
//         <h1>State: ${data.state}</h1>
//         <h4>Sensors:</h4>
//         <ul>${sensorsHtml}</ul>
//         <h4>Servos:</h4>
//         <ul>${servosHtml}</ul>
//         <h4>Relays:</h4>
//         <ul>${relaysHtml}</ul>
//         <h4>Velocity: ${data.velocity} m/s</h4>
//         <pre>${data["="]}</pre>
//     `;
// });

// source.addEventListener("error", function (event) {
//     try {
//         const data = JSON.parse(event.data);
//         console.log("Error: ", data);
//         const container = document.querySelector('#rocket-progress');

//         container.innerHTML = `
//             <h3>${data.status}</h3>
//             <p>Message: ${data.message} </p>
//             `;
//     } catch (e) {
//         console.error("Error parsing SSE data:", e);
//     }

//     source.close();

//     console.warn("Połączenie SSE zostało zamknięte po błędzie.");
// });

