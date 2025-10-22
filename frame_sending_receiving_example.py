from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError

def on_altitude(frame: Frame):
    print(f"Registered frame received: {frame}")

if __name__ == "__main__":
    max_altitude = 0.0
    g = 9.81
    v_max = 30
    heater_open = False
    cm = CommunicationManager() # Class responsible for communication handling
    cm.change_transport_type(TransportType.TCP)
    # We must create a frame that will serve as a pattern indicating what kind of frames we want to receive
    # During frame equality comparison the following fields are excluded: priority, data_type, payload
    # You can find more information in communication_library/frame.py

    altitude_frame = Frame(ids.BoardID.SOFTWARE, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.FEED, 
                           ids.BoardID.ROCKET, 
                           ids.DeviceID.SENSOR, 
                           2, # altitude sensor
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.SENSOR.value.READ)

    oxidizer_pressure_frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    3, # oxidizer pressure
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)

    oxidizer_level_frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    1, # oxidizer level
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
    cm.register_callback(on_altitude, oxidizer_level_frame)

    fuel_level_frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    0, # fuel level
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
    
    angle_frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    4, # angle
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)

    cm.connect(TcpSettings("127.0.0.1", 3000))

    oxidizer_heater_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           0, # oxidizer heater
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN,
                           ()
                           )
    
    #cm.push(oxidizer_heater_open_frame) # We need to push the frame onto the send queue
    #cm.send() # Send queue first in the send queue

    oxidizer_heater_close_frame = oxidizer_heater_open_frame.reverse_servos_relays_status()


    oxidizer_intake_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           1, # oxidizer intake 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,) # 0 is for open position, 100 is for closed
                           )
    cm.push(oxidizer_intake_open_frame)
    cm.send()
    
    oxidizer_intake_close_frame = oxidizer_intake_open_frame.reverse_servos_relays_status()

    fuel_intake_open_frame = Frame(ids.BoardID.ROCKET,
                                   ids.PriorityID.LOW,
                                   ids.ActionID.SERVICE,
                                   ids.BoardID.SOFTWARE,
                                   ids.DeviceID.SERVO,
                                   0,
                                   ids.DataTypeID.INT16,
                                   ids.OperationID.SERVO.value.POSITION,
                                   (0,))
    
    fuel_intake_close_frame = fuel_intake_open_frame.reverse_servos_relays_status()


    fuel_main_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           2, # fuel main 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,) # 0 is for open position, 100 is for closed
                           )
    fuel_main_close_frame = fuel_main_open_frame.reverse_servos_relays_status()

    oxidizer_main_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.SERVO, 
                           3, # oxidizer main 
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,) # 0 is for open position, 100 is for closed
                           )
    oxidizer_main_close_frame = oxidizer_main_open_frame.reverse_servos_relays_status()

    igniter_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           1, # igniter
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN,
                           ())
    igniter_close_frame = igniter_open_frame.reverse_servos_relays_status()

    parachute_open_frame = Frame(ids.BoardID.ROCKET, 
                           ids.PriorityID.LOW, 
                           ids.ActionID.SERVICE, 
                           ids.BoardID.SOFTWARE, 
                           ids.DeviceID.RELAY, 
                           2, # parachute
                           ids.DataTypeID.FLOAT,
                           ids.OperationID.RELAY.value.OPEN,
                           ())
    parachute_close_frame = parachute_open_frame.reverse_servos_relays_status()

    while True:
        try:
            frame = cm.receive() # We can handle frames using callbacks or by getting frame right from receive() call
            frame_dict = frame.as_dict()

            # wyłączenie podgrzewania i start rakiety
            if frame_dict["device_id"] == 3 and frame_dict["payload"][0] > 60.0 and max_altitude == 0.0:
                #cm.unregister_callback(oxidizer_pressure_frame)
                print("Oxidizer pressure heater is 60 bar.")
                cm.push(oxidizer_heater_close_frame)
                cm.send()
                heater_open = False

                cm.register_callback(on_altitude, altitude_frame)
                cm.register_callback(on_altitude, angle_frame)
                cm.push(fuel_main_open_frame)
                cm.send()

                cm.push(oxidizer_main_open_frame)
                cm.send()

                cm.push(igniter_open_frame)
                cm.send()


            # wyłączenie utleniacza i włączenie dopływu paliwa
            if frame_dict["device_id"] == 1 and  frame_dict["payload"][0] == 100:
                cm.unregister_callback(oxidizer_level_frame)
                print("Oxidizer level is 100")
                cm.push(oxidizer_intake_close_frame)
                cm.send()
                
                cm.register_callback(on_altitude, fuel_level_frame)
                cm.push(fuel_intake_open_frame)
                cm.send()
            
            # wyłączenie dopływu paliwa i włączenie podgrzewania
            if frame_dict["device_id"] == 0 and frame_dict["payload"][0] == 100:
                cm.unregister_callback(fuel_level_frame)
                print("Fuel level is 100")
                cm.push(fuel_intake_close_frame)
                cm.send()

                cm.register_callback(on_altitude, oxidizer_pressure_frame)
                cm.push(oxidizer_heater_open_frame)
                cm.send()
                heater_open = True
            
            # ustawienie maksymalnej wysokości
            if frame_dict["device_id"] == 2 and frame_dict["payload"][0] > max_altitude:
                max_altitude = frame_dict["payload"][0]

            # wyliczenie wysokości otwarcia spadochronu i otwarcie spadochronu
            if frame_dict["device_id"] == 2 and frame_dict["payload"][0] < max_altitude:
                h2 = (2*max_altitude*g - (v_max)**2)/(2*g)
                print(max_altitude, h2)
                current_height = frame_dict["payload"][0]
                cm.push(igniter_close_frame)
                cm.send()
                cm.push(fuel_main_close_frame)
                cm.send()
                cm.push(oxidizer_main_close_frame)
                cm.send()
                if current_height <= h2:
                    cm.push(parachute_open_frame)
                    cm.send()
                    cm.unregister_callback(altitude_frame)
            
            # wyłączenie podgrzewania 
            if frame_dict["device_id"] == 3 and frame_dict["payload"][0] >= 65.0 and heater_open == True:
                cm.push(oxidizer_heater_close_frame)
                cm.send()
                heater_open = False

            # włączenie podgrzewania 
            if frame_dict["device_id"] == 3 and frame_dict["payload"][0] <= 55.0 and heater_open == False:
                cm.push(oxidizer_heater_open_frame)
                cm.send()
                heater_open = True

        except TransportTimeoutError:
            pass
        except UnregisteredCallbackError as e:
            continue
            #print(f"unregistered frame received: {e.frame}")
    