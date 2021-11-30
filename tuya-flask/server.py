from flask import Flask, request, jsonify
import tuya

# setup flask
api = Flask(__name__)

# Get All Devices
@api.route('/devices', methods=['GET'])
def getDevices():
    return tuya.getAllDevices()

# Get Device By Id
@api.route('/device/<id>', methods=['GET'])
def get_device(id):
    return tuya.getDevice(id)

# Get Device Inst. Set

# Turn Light On/Off
@api.route('/control/switch/<id>/<value>', methods=['POST'])
def post_control_switch(id, value):
    isOn = value == "on"
    return tuya.lightOnOff(id, isOn)

# Toggle Light
@api.route('/control/toggle/<id>', methods=['POST'])
def post_control_toggle(id):
    return tuya.toggleLight(id)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=1234)