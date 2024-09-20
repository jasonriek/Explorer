from flask import Flask, request
from drivers.L298N import forwardDrive, reverseDrive, allStop, forwardTurnLeft, forwardTurnRight

app = Flask(__name__)

@app.route('/motor', methods=['POST'])
def control_motor():
    direction = request.json.get('direction')
    
    if direction == 'forward':
        forwardDrive()
    elif direction == 'reverse':
        reverseDrive()
    elif direction == 'turn_left':
        forwardTurnLeft()
    elif direction == 'turn_right':
        forwardTurnRight()
    elif direction == 'stop':
        allStop()
    else:
        return {'status': 'invalid direction'}, 400
    
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
