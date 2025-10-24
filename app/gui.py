from nicegui import ui

# Słownik przechowujący aktualne przypisania puzzli do slotów
current_positions = {}

# Poprawne pozycje
correct_positions = {
    "puzzle1": "slot1",
    "puzzle2": "slot2",
    "puzzle3": "slot3",
}

def check_result():
    if current_positions == correct_positions:
        ui.notify("✅ Ułożenie poprawne!", color="green")
    else:
        ui.notify("❌ Coś jest nie tak.", color="red")

# Funkcja aktualizująca pozycje z JS
ui.label("🧩 Ułóż puzzle w odpowiednie miejsca").classes("text-h5 mb-4")

ui.html('''
<style>
    .container { display: flex; justify-content: space-around; margin-bottom: 40px; }
    .puzzle {
    width: 100px; height: 100px;
    background-color: #b2f5b2;
    text-align: center; line-height: 100px;
    border: 2px solid #006400; border-radius: 10px;
    cursor: grab; user-select: none;
    }
    .slot {
    width: 110px; height: 110px;
    border: 2px dashed gray;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    }
    .slot.highlight {
    border-color: #00a000;
    }
</style>

<div class="container" id="puzzle-container">
    <div id="puzzle1" class="puzzle" draggable="true">Puzzle 1</div>
    <div id="puzzle2" class="puzzle" draggable="true">Puzzle 2</div>
    <div id="puzzle3" class="puzzle" draggable="true">Puzzle 3</div>
</div>

<div class="container" id="slot-container">
    <div id="slot1" class="slot"></div>
    <div id="slot2" class="slot"></div>
    <div id="slot3" class="slot"></div>
</div>
''', sanitize=False)

ui.add_body_html("""
<script>
    const puzzles = document.querySelectorAll('.puzzle');
    const slots = document.querySelectorAll('.slot');
    let dragged = null;

    puzzles.forEach(p => {
    p.addEventListener('dragstart', e => {
        dragged = p;
        e.dataTransfer.setData('text', p.id);
    });
    });

    slots.forEach(slot => {
    slot.addEventListener('dragover', e => e.preventDefault());
    slot.addEventListener('dragenter', e => slot.classList.add('highlight'));
    slot.addEventListener('dragleave', e => slot.classList.remove('highlight'));
    slot.addEventListener('drop', e => {
        e.preventDefault();
        slot.classList.remove('highlight');
        if (dragged) {
        slot.innerHTML = '';
        slot.appendChild(dragged);
        // wyślij dane do NiceGUI
        window.sendEvent('update_position', {puzzle: dragged.id, slot: slot.id});
        }
    });
    });
</script>
""")

    # Obsługa zdarzenia z JS
def handle_update(event):
    puzzle = event.args['puzzle']
    slot = event.args['slot']
    current_positions[puzzle] = slot
    ui.notify(f'{puzzle} -> {slot}')

ui.on('update_position', handle_update)

ui.button("Sprawdź", on_click=check_result).classes("mt-4")

# Uruchom
ui.run()
