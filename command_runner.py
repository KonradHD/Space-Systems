import subprocess
from commands import Command


def run_commands(slots):
    
    
    cmd = Command()
    for slot in slots:
        if slot == "Open oxidizer intake":
            cmd.open_oxidizer_intake()
        if slot == "Register oxidizer level":
            cmd.register_oxidizer_level()
        if slot == "Wait till oxidizer level will be 100%":
            cmd.wait_till_oxidizer_level()
        if slot == "Close oxidizer intake":
            cmd.close_oxidizer_intake()
        if slot == "Unregister oxidizer level":
            cmd.unregister_oxidizer_intake()
        if slot == "Open fuel intake":
            cmd.open_fuel_intake()