import argparse
import threading
import time
from pathlib import Path

DURATION = 30  # in seconds


class AnObject:
    def __init__(self, sn):
        self.sn = sn

    def get_control_pilot_details(self):
        return f"Here are the details of Control Pilot: {self.sn} \n"


class BasicClass:
    def __init__(self):
        self.database_log = True  # logging enabled
        self.sn_ip = None  # devices configured
        self.threads = []  # list of logging threads started

    def log_device_from_db(self, device, output_path, *args):
        """Log pilot details every second of a specific device in a file"""
        with open(output_path / Path(f"{device}_db.log"), "a") as log:
            while self.database_log:  # don't stop while logging is enabled
                log.write(self.sn_ip[device]["database"].get_control_pilot_details())
                time.sleep(1)

    def init_log_for_register_devices(self, output_path=Path("")):
        """Starts the logging process"""
        self.database_log = True  # make sure logging is marked as enabled
        # setup devices to log
        self.sn_ip = {
            "SN01": {"database": AnObject("SN01")},
            "SN02": {"database": AnObject("SN01")},
        }
        # start a thread for the logging mechanism for every device
        for device in self.sn_ip:
            t = threading.Thread(
                group=None,
                target=self.log_device_from_db,
                name=f"Logging data for device: {device}",
                args=(device, output_path),
            )
            self.threads.append(t)
            t.daemon = True
            t.start()

    def stop_log(self):
        """Stops logging process"""
        self.database_log = False  # make every thread to notice that they should finish looping
        # wait for all threads to finish
        for thread in self.threads:
            thread.join()


if __name__ == "__main__":
    # configure inline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default="")
    args = parser.parse_args()

    my_object = BasicClass()
    my_object.init_log_for_register_devices(args.output)  # start logging

    time_to_end = time.time() + DURATION
    while time.time() < time_to_end:  # wait specific amount of time
        pass
    my_object.stop_log()  # stop logging

"""
    Part 1:
    Explain what this script does inside the own code.
        Done.

    Part 2:
    The code is unfinished, it is mandatory that after 30s the program stops safely, can you modify the code in order
    to achieve that requirement?
        Done.

    Part 3:
    Our stakeholder needs to make the logs path configurable, can you modify the code in order to make the log paths
    configurable asking them through command line?
        Sure, give it a try: python3 python_test.py --output your_path/

    Part 4:
    How could the main functionality of the script be improved?
        One thing I see is that the log file is written using a context manager, which is the way to go since it would
        allow you to allocate and release resources precisely like in this case, close the file when done without
        having to do it explicitly.
        
        The issue here is that this logging process could last for quite some time, so, this means that the content of
        the file would not be available until all the process finishes which can be annoying, but can be even dangerous
        if the execution gets stopped by whatever reason since you could end with an incomplete/blank/corrupt log file. 
        
        One way to fix this could be to add `log.flush()` right after using `log.write`, this would force to
        clear the internal buffer and save the content of that line in the file straightway.
        
    Note: There is not just one solution for this test, you can proceed as you wish but the main functionality of the 
    script has to be conserved
"""
