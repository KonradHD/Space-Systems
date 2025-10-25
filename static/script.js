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

//--- DRAG & DROP NA SLOTY ---
/* function enableDropZones(zoneList) {
    zoneList.forEach(vslot => {
        vslot.addEventListener('dragover', e => e.preventDefault());

        vslot.addEventListener('dragenter', () => {
            // podświetlenie tylko jeśli slot pusty
            if (!vslot.firstChild) vslot.classList.add('highlight');
        });

        vslot.addEventListener('dragleave', () => {
            vslot.classList.remove('highlight');
        });

        vslot.addEventListener('drop', e => {
            e.preventDefault();
            vslot.classList.remove('highlight');

            // jeśli slot ma już element — nie przyjmuj nowego
            // if (vslot.firstChild) return;
            if (vslot.firstChild && vslot.firstChild !== dragged) return;

            if (dragged) {
                const oldParent = dragged.parentElement;
                // jeśli stary slot był pusty po zabraniu, pozwól wrócić do homeContainer
                oldParent.classList.remove('highlight');
                vslot.appendChild(dragged);
            }
        });
    });
} */

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
    const current = Array.from(vslots).map(vslot => vslot.textContent.trim());
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

pollOxidizerData("/api/oxidizer_data");

