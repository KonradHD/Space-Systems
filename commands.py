from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError
import time



#frame_dict["device_type"] == 2 SENSOR
#frame_dict["device_type"] == 1 RELAY
#frame_dict["device_type"] == 0 SERVO

def on_altitude(frame: Frame):
    print(f"Registered frame received: {frame}")

class Command():

    def __init__(self):
        self.oxidizer_level_data = {
            "data" : [],
            "time" : 0
        }
        self.cm = CommunicationManager()
        self.cm.change_transport_type(TransportType.TCP)

        self.oxidizer_intake_open = False
        self.fuel_intake_open = False
        self.oxidizer_heater_open = False
        self.fuel_main_valve_open = False
        self.oxidizer_main_valve_open = False
        self.igniter_open = False
        self.parachute_open = False
        

    def connect(self):
        self.cm.connect(TcpSettings("127.0.0.1", 3000)) 


    def get_oxidizer_level_data(self):
        return self.oxidizer_level_data

    def open_oxidizer_intake(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           1, # oxidizer intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,))
        self.cm.push(frame)
        self.cm.send()
        


    def register_oxidizer_level(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    1, # oxidizer level
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.register_callback(on_altitude, frame)


    def receive_frame(self) -> Frame:
        return self.cm.receive()
    

    def wait_till_oxidizer_level(self, value) -> bool:
        print("wait_till_oxidizer_level")
        start_time = time.time()
        timeout = 20

        while time.time() - start_time <= timeout:
            try:
                frame = self.cm.receive()
                frame_dict = frame.as_dict()
                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 1:
                    self.oxidizer_level_data["data"].append(frame_dict["payload"][0])
                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 1 and frame_dict["payload"][0] >= float(value):
                    self.close_oxidizer_intake()
                    self.oxidizer_level_data["time"] = time.time() - start_time
                    return True
            except TransportTimeoutError:
                pass
            except UnregisteredCallbackError as e:
                continue
            except Exception as e:
                print(f"Time waiting error: {e}")
                continue 
        return False
    

    def close_oxidizer_intake(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           1, # oxidizer intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (100,))
        self.cm.push(frame)
        self.cm.send()

    
    def unregister_oxidizer_level(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    1, # oxidizer level
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.unregister_callback(frame)

    def open_fuel_intake(self):
        frame = Frame(ids.BoardID.ROCKET,
                                   ids.PriorityID.LOW,
                                   ids.ActionID.SERVICE,
                                   ids.BoardID.SOFTWARE,
                                   ids.DeviceID.SERVO,
                                   0,
                                   ids.DataTypeID.INT16,
                                   ids.OperationID.SERVO.value.POSITION,
                                   (0,))
        self.cm.push(frame)
        self.cm.send()
        self.fuel_intake_open = True
    
    def register_fuel_level(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    0, # fuel level
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.register_callback(on_altitude, frame)

    def wait_till_fuel_level(self, value) -> bool:
        start_time = time.time()
        timeout = 20

        while time.time() - start_time <= timeout:
            try:
                frame = self.cm.receive()
                frame_dict = frame.as_dict()
                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 0 and frame_dict["payload"][0] >= float(value):
                    self.close_fuel_intake()
                    return True
            except TransportTimeoutError:
                pass
            except UnregisteredCallbackError as e:
                continue
            except Exception as e:
                print(f"Time waiting error: {e}")
                continue 
        return False
    
    def close_fuel_intake(self):
        frame = Frame(ids.BoardID.ROCKET,
                                   ids.PriorityID.LOW,
                                   ids.ActionID.SERVICE,
                                   ids.BoardID.SOFTWARE,
                                   ids.DeviceID.SERVO,
                                   0,
                                   ids.DataTypeID.INT16,
                                   ids.OperationID.SERVO.value.POSITION,
                                   (100,))
        self.cm.push(frame)
        self.cm.send()

    def unregister_fuel_level(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    0, # fuel level
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.unregister_callback(frame)


    def register_oxidizer_pressure(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    3, # oxidizer pressure
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.register_callback(on_altitude, frame)

    def open_oxidizer_heater(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           0, # oxidizer heater
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN,
                           ())
        self.cm.push(frame)
        self.cm.send()
        self.oxidizer_heater_open = True


    def wait_till_oxidizer_pressure(self, value) -> bool:
        start_time = time.time()
        timeout = 15

        while time.time() - start_time <= timeout:
            try:
                frame = self.cm.receive()
                frame_dict = frame.as_dict()
                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 3 and frame_dict["payload"][0] >= float(value):
                    self.close_oxidizer_heater()
                    return True
            except TransportTimeoutError:
                pass
            except UnregisteredCallbackError as e:
                continue
            except Exception as e:
                print(f"Time waiting error: {e}")
                continue 
        return False
    
    def close_oxidizer_heater(self):
        frame = frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           0, # oxidizer heater
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.CLOSE,
                           ())
        self.cm.push(frame)
        self.cm.send()


    def unregister_oxidizer_pressure(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    3, # oxidizer pressure
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.unregister_callback(frame)

    def open_fuel_main_valve(self): 
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           2, # fuel main 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,))
        self.cm.push(frame)
        self.cm.send()

    def open_oxidizer_main_valve(self): 
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           3, # oxidizer main 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,)) # 0 is for open position, 100 is for closed
        self.cm.push(frame)
        self.cm.send()


    def open_igniter(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           1, # igniter
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN,
                           ())
        self.cm.push(frame)
        self.cm.send()


    def wait_till_reach_apogeum(self) -> bool:
        start_time = time.time()
        timeout = 30
        max_height = 0

        while time.time() - start_time <= timeout:
            try:
                frame = self.cm.receive()
                frame_dict = frame.as_dict()
                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 2 and frame_dict["payload"][0] > max_height:
                    max_height = frame_dict["payload"][0]

                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 2 and frame_dict["payload"][0] < max_height:
                    return True
            except TransportTimeoutError:
                pass
            except UnregisteredCallbackError as e:
                continue
            except Exception as e:
                print(f"Time waiting error: {e}")
                continue 
        return False
    

    def wait_till_rocket_fall(self, fall_distance) -> bool:
        start_time = time.time()
        timeout = 30

        while time.time() - start_time <= timeout:
            try:
                frame = self.cm.receive()
                frame_dict = frame.as_dict()
                current_height = frame_dict["payload"][0]
                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 2 and current_height > max_height:
                    max_height = frame_dict["payload"][0]

                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 2 and current_height < max_height:
                    if current_height <= max_height - float(fall_distance):
                        return True
            except TransportTimeoutError:
                pass
            except UnregisteredCallbackError as e:
                continue
            except Exception as e:
                print(f"Time waiting error: {e}")
                continue 
        return False
    

    def close_igniter(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           1, # igniter
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.CLOSE,
                           ())
        self.cm.push(frame)
        self.cm.send()


    def close_oxidizer_main_valve(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           3, # oxidizer main 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (100,)) # 0 is for open position, 100 is for closed
        self.cm.push(frame)
        self.cm.send()


    def close_fuel_main_valve(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           2, # fuel main 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (100,))
        self.cm.push(frame)
        self.cm.send()

    def register_angle(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    4, # angle
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.register_callback(on_altitude, frame)


    def register_altitude(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    2, # altitude
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.register_callback(on_altitude, frame)


    def open_parachute(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           2, # parachute
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN,
                           ())
        self.cm.push(frame)
        self.cm.send()


    def close_parachute(self):
        frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           2, # parachute
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.CLOSE,
                           ())
        self.cm.push(frame)
        self.cm.send()


    def unregister_angle(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    4, # angle
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.unregister_callback(frame)


    def unregister_altitude(self):
        frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    2, # altitude
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
        self.cm.unregister_callback(frame)


    def wait_till_rocket_land(self) -> bool:
        start_time = time.time()
        timeout = 180
        max_height = 0

        while time.time() - start_time <= timeout:
            try:
                frame = self.cm.receive()
                frame_dict = frame.as_dict()
                current_height = frame_dict["payload"][0]
                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 2 and current_height > max_height:
                    max_height = frame_dict["payload"][0]

                if frame_dict["device_type"] == 2 and frame_dict["device_id"] == 2 and current_height < max_height and current_height == 0:
                    return True
                print(max_height, current_height)
            except TransportTimeoutError:
                pass
            except UnregisteredCallbackError as e:
                continue
            except Exception as e:
                print(f"Time waiting error: {e}")
                continue 
        return False


    def reset(self):
        self.unregister_altitude()
        self.unregister_angle()
        self.unregister_fuel_level()
        self.unregister_oxidizer_level()
        self.unregister_oxidizer_pressure()