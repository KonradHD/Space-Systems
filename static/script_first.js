const buttons = document.querySelectorAll('.answer');
const slots = document.querySelectorAll('.slot');
let dragged = null;

buttons.forEach(btn => {
    btn.addEventListener('dragstart', e => {
        dragged = btn;
        e.dataTransfer.effectAllowed = "move";
    });
});

slots.forEach(slot => {
    slot.addEventListener('dragover', e => e.preventDefault());

    slot.addEventListener('dragenter', () => {
        slot.classList.add('highlight');
    });

    slot.addEventListener('dragleave', () => {
        slot.classList.remove('highlight');
    });

    slot.addEventListener('drop', e => {
        e.preventDefault();
        slot.classList.remove('highlight');
        if (dragged) {
            // usuń poprzedni element ze slota
            slot.innerHTML = '';
            slot.appendChild(dragged);
        }
    });
});

document.getElementById('check').addEventListener('click', () => {
    const current = Array.from(slots).map(slot => slot.textContent.trim());
    const correct = [
        "Open oxidizer",
        "Open fuel intake",
        "Ignite engines",
        "Close fuel intake",
        "Close oxidizer",
        "Launch rocket"
    ];

    if (JSON.stringify(current) === JSON.stringify(correct)) {
        alert("✅ Rakieta gotowa do startu!");
    } else {
        alert("❌ Coś poszło nie tak. Spróbuj jeszcze raz!");
    }
});
