const buttons = document.querySelectorAll('.answer');
const vslots = document.querySelectorAll('.valid-slot');
const homeContainer = document.querySelector('.buttons-container');
const homeSlots = document.querySelectorAll(".slot")
let dragged = null;
let ghost = null;

// --- DRAG START ---
buttons.forEach(btn => {
    btn.addEventListener('dragstart', e => {
        dragged = btn;

        // Ustawienie przezroczystego "ducha", który porusza się z kursorem
        ghost = btn.cloneNode(true);
        ghost.style.position = 'absolute';
        ghost.style.pointerEvents = 'none';
        ghost.style.opacity = '0.6';
        ghost.style.zIndex = '1000';
        document.body.appendChild(ghost);

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
});

//--- DRAG & DROP NA SLOTY ---
function enableDropZones(zoneList) {
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
            if (vslot.firstChild) return;

            if (dragged) {
                const oldParent = dragged.parentElement;
                // jeśli stary slot był pusty po zabraniu, pozwól wrócić do homeContainer
                oldParent.classList.remove('highlight');
                vslot.appendChild(dragged);
            }
        });
    });
}

// Aktywujemy obsługę dla slotów i początkowej sekcji
enableDropZones(vslots);
enableDropZones([homeContainer]);
enableDropZones(homeSlots)

// --- SPRAWDZENIE UŁOŻENIA ---
document.getElementById('check').addEventListener('click', () => {
    const current = Array.from(vslots).map(vslot => vslot.textContent.trim());
    // wysyłka do backendu
    fetch('/api/check', { // <- Twój endpoint backendowy
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
