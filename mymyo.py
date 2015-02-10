import myo
from myo.lowlevel import stream_emg


class MyMyo:
    def __init__(self, callback):
        self.hub = None
        self.myo = None
        self.init(callback)

    def __del__(self):
        if self.hub:
            self.hub.stop(True)

    def init(self, callback):
        myo.init()
        self.hub = myo.Hub()
        self.hub.set_locking_policy(myo.locking_policy.none)
        self.myo = self.MyoListener(self)
        self.myo.callback = callback
        myo.set_stream_emg(stream_emg.enabled)
        self.hub.run(1000, self.myo)

    class MyoListener(myo.DeviceListener):
        def __init__(self, managment):
            self.callback = None
            self.rssi = None
            self.connected = False
            self.paired = False
            self.synched = False
            self.managment = managment

        def on_connect(self, myo, timestamp):
            myo.vibrate('short')
            self.connected = True
            myo.request_rssi()

        def on_rssi(self, myo, timestamp, rssi):
            self.rssi = rssi

        def on_pair(self, myo, timestamp):
            self.paired = True

        def on_disconnect(self, myo, timestamp):
            self.connected = False

        def on_sync(self, myo, timestamp, arm, x_direction):
            self.synched = True

        def on_unsync(self, myo, timestamp):
            self.synched = False

        def on_emg(self, myo, timestamp, emg):
            if self.callback:
                self.callback(emg)


if __name__ == '__main__':
    my = MyMyo()