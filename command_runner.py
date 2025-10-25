from commands import Command
from time import sleep
from flask import Blueprint, jsonify

class Runner():

    def __init__(self):
        self.cmd = Command()
        self.oxidizer_level = False
        self.fuel_level = False
        self.oxidizer_pressure = False
        self.reach_apogeum = False
        self.fall_meters = False
        self.landed = False


    def run_commands(self, slots):
        sleep(2)
        for slot in slots:
            if len(slot.split(" ")) < 5 and slot != "":
                fun = slot.lower().replace(" ", "_")
                getattr(self.cmd, fun)()
            else:
                if slot.startswith("Wait till oxidizer level will be"):
                    self.oxidizer_level = self.cmd.wait_till_oxidizer_level(100)
                    if not self.oxidizer_level:
                        print("Timeout")
                        break
                if slot.startswith("Wait till fuel level will be"):
                    self.fuel_level = self.cmd.wait_till_fuel_level(100)
                    if not self.fuel_level:
                        print("Timeout")
                        break
                if slot.startswith("Wait till the oxidizer pressure will be"):
                    self.oxidizer_pressure = self.cmd.wait_till_oxidizer_pressure(60)
                    if not self.oxidizer_pressure:
                        print("Timeout")
                        break
                if slot == "Wait till the rocket will reach apogeum":
                    self.reach_apogeum = self.cmd.wait_till_reach_apogeum()
                    if not self.reach_apogeum:
                        print("Timeout")
                        break
                if slot.startswith("Wait till the oxidizer pressure will be"):
                    self.fall_meters = self.cmd.wait_till_rocket_fall(40)
                    if not self.fall_meters:
                        print("Timeout")
                        break
                if slot == "Wait till rocket will land":
                    self.landed = self.cmd.wait_till_rocket_land()
                    if not self.landed:
                        print("Timeout")
                        break
                    print("Rakieta bezpiecznie wylądowała!") ## poprawić (przesłać informacje z simulatora do frontendu)
