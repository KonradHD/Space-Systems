from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError
import time

def on_altitude(frame: Frame):
    print(f"Registered frame received: {frame}")

class Command():

    def __init__(self):
        self.cm = CommunicationManager()
        self.cm.change_transport_type(TransportType.TCP)
        self.cm.connect(TcpSettings("127.0.0.1", 3000))


    def get_CommunicatianManager(self):
        return self.cm




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
        start_time = time.time()
        timeout = 15

        while time.time() - start_time <= timeout:
            try:
                frame = self.cm.receive()
                frame_dict = frame.as_dict()
                if frame_dict["device_id"] == 1 and frame_dict["payload"][0] == value:
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

    
    def unregister_oxidizer_intake(self):
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