from commands import Command
from time import sleep
from flask import Blueprint, jsonify

class Runner():

    def __init__(self):
        self.cmd = Command()
        self.data = {}
        self.parachute_open = False
        self.landed = False


    def run_commands(self, slots):
        self.cmd.connect()
        sleep(2)
        for slot in slots:
            if slot["type"] == "void non parametric":
                fun = slot["name"].lower().replace(" ", "_")
                getattr(self.cmd, fun)()
            if slot["type"] == "bool non parametric":
                if slot["name"] == "Wait till the rocket will reach apogeum":
                    reach_apogeum = self.cmd.wait_till_reach_apogeum()
                    if not reach_apogeum:
                        print("Timeout")
                        return 1
                if "parachute" in slot["name"].split(" "):
                    fun = slot["name"].lower().replace(" ", "_")
                    self.parachute_open = getattr(self.cmd, fun)()
                if slot["name"] == "Wait till rocket will land":
                    self.landed = self.cmd.wait_till_rocket_land()
                    if not self.landed:
                        print("Timeout")
                        return 1
                print("Rakieta bezpiecznie wylądowała!")
            else:
                if slot["value"] == "":
                    raise ValueError("Cannot convert empty string to float")
                if slot["name"].startswith("Wait till oxidizer level will be"):
                    oxidizer_level = self.cmd.wait_till_oxidizer_level(slot["value"])
                    if not oxidizer_level:
                        print("Timeout")
                        return 1
                if slot["name"].startswith("Wait till fuel level will be"):
                    fuel_level = self.cmd.wait_till_fuel_level(slot["value"])
                    if not fuel_level:
                        print("Timeout")
                        return 1
                if slot["name"].startswith("Wait till the oxidizer pressure will be"):
                    oxidizer_pressure = self.cmd.wait_till_oxidizer_pressure(slot["value"])
                    if not oxidizer_pressure:
                        print("Timeout")
                        return 1
                if slot["name"].startswith("Wait till the rocket will fall"):
                    fall_meters = self.cmd.wait_till_rocket_fall(slot["value"])
                    if not fall_meters:
                        print("Timeout")
                        return 1
                if slot["name"].startswith("Sleep for"):
                    sleep(float(slot["value"]))

        if self.landed == False and self.parachute_open == True:
            return 2
        return 0


    def reset(self):
        self.cmd.reset()
        self.parachute_open = False
        self.landed = False

    def get_data(self):
        return self.cmd.data
