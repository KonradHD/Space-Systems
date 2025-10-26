from commands import Command
from time import sleep
from flask import Blueprint, jsonify

class Runner():

    def __init__(self):
        self.cmd = Command()


    def run_commands(self, slots):
        self.cmd.connect()
        sleep(2)
        for slot in slots:
            if slot["type"] == "void non parametric":
                fun = slot["name"].lower().replace(" ", "_")
                getattr(self.cmd, fun)()
            else:
                if slot["value"] == "":
                    raise ValueError("Cannot convert empty string to float")
                if slot["name"].startswith("Wait till oxidizer level will be"):
                    oxidizer_level = self.cmd.wait_till_oxidizer_level(slot["value"])
                    if not oxidizer_level:
                        print("Timeout")
                        return "Timeout"
                if slot["name"].startswith("Wait till fuel level will be"):
                    fuel_level = self.cmd.wait_till_fuel_level(slot["value"])
                    if not fuel_level:
                        print("Timeout")
                        return "Timeout"
                if slot["name"].startswith("Wait till the oxidizer pressure will be"):
                    oxidizer_pressure = self.cmd.wait_till_oxidizer_pressure(slot["value"])
                    if not oxidizer_pressure:
                        print("Timeout")
                        return "Timeout"
                if slot["name"] == "Wait till the rocket will reach apogeum":
                    reach_apogeum = self.cmd.wait_till_reach_apogeum()
                    if not reach_apogeum:
                        print("Timeout")
                        return "Timeout"
                if slot["name"].startswith("Wait till the rocket will fall"):
                    fall_meters = self.cmd.wait_till_rocket_fall(slot["value"])
                    if not fall_meters:
                        print("Timeout")
                        return "Timeout"
                if slot["name"].startswith("Sleep for"):
                    sleep(float(slot["value"]))
                if slot["name"] == "Wait till rocket will land":
                    landed = self.cmd.wait_till_rocket_land()
                    if not landed:
                        print("Timeout")
                        return "Timeout"
                    print("Rakieta bezpiecznie wylądowała!")
        return "Koniec pętli"
    def reset(self):
        self.cmd.reset()
