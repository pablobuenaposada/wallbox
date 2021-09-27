import threading
import time


class AnObject:
    def __init__(self, sn):
        self.sn = sn

    def get_control_pilot_details(self):
        return f"Here are the details of Control Pilot: {self.sn} \n"


class BasicClass:
    def __init__(self):
        self.database_log = True
        self.sn_ip = None
        self.threads = []

    def log_device_from_db(self, device, *args):
        with open(f'{device}_db.log', 'a') as log:
            while self.database_log:
                log.write(self.sn_ip[device]["database"].get_control_pilot_details())
                time.sleep(1)

    def init_log_for_register_devices(self):
        self.database_log = True
        self.sn_ip = {"SN01": {'database': AnObject("SN01")},
                      "SN02": {'database': AnObject("SN01")}}
        for device in self.sn_ip:
            t = threading.Thread(group=None,
                                 target=self.log_device_from_db,
                                 name=f"Logging data for device: {device}",
                                 args=(device,)
                                 )
            self.threads.append(t)
            t.daemon = True
            t.start()


if __name__ == '__main__':
    my_object = BasicClass()
    my_object.init_log_for_register_devices()
    while True:
        pass


"""
    Part 1:
    Explain what this script does inside the own code.
    
    Part 2:
    The code is unfinished, it is mandatory that after 30s the program stops safely, can you modify the code in order
    to achieve that requirement?
    
    Part 3:
    Our stakeholder needs to make the logs path configurable, can you modify the code in order to make the log paths
    configurable asking them through command line?
    
    Part 4:
    How could the main functionality of the script be improved?
    
    Note: There is not just one solution for this test, you can proceed as you wish but the main functionality of the 
    script has to be conserved
"""
