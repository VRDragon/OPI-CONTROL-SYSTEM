import RPi.GPIO as GPIO
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
import time

def create_app(configfile='server.cfg'):
    app = Flask(__name__)
    AppConfig(app, configfile)
    app.debug = app.config['DEBUG']
    Bootstrap(app)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Grab all pins from the configuration file
    pins = app.config['PINS']
    # Set each pin as an output and make it low
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    @app.route('/')
    def index():
        # For each pin, read the pin state and store it in the pins dictionary
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary
        templateData = {
            'pins' : pins
        }
        return render_template('index.html', **templateData)

    # The function below is executed when someone requests a URL without a
    # pin number -> master control for all pins
    @app.route('/<master>')
    def master(master):
        if master == 'on':
            # Set all pins to high
            for pin in pins:
                GPIO.output(pin, GPIO.HIGH)
            message = 'Turned all interfaces on.'
        if master == 'off':
            # Set all pins to low
            for pin in pins:
                GPIO.output(pin, GPIO.LOW)
            message = 'Turned all interfaces off.'
        # For each pin, read the pin state and store it in the pins dictionary
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Along with the pin dictionary, put the message into the template data dictionary
        templateData = {
                        'message' : message,
                        'pins' : pins
                        }
        return render_template('index.html', **templateData)

    # The function below is executed when someone requests a URL with the
    # pin number and action in it
    @app.route('/<changePin>/<action>')
    def action(changePin, action):
        # Convert the pin from the URL into an integer
        changePin = int(changePin)
        # Get the device name for the pin being changed
        deviceName = pins[changePin]['name']
        # If the action part of the URL is "on," execute the code indented below
        if action == 'on':
            # Set the pin high
            GPIO.output(changePin, GPIO.HIGH)
            # Save the status message to be passed into the template
            message = 'Turned ' + deviceName + ' on.'
        if action == 'off':
            GPIO.output(changePin, GPIO.LOW)
            message = 'Turned ' + deviceName + ' off.'
        if action == 'toggle':
            # Read the pin and set it to whatever it isn't (that is, toggle it)
            GPIO.output(changePin, not GPIO.input(changePin))
            message = 'Toggled ' + deviceName + '.'
        if action == 'reset':
            # Set the pin to low and after 5 s back to high
            GPIO.output(changePin, GPIO.LOW)
            time.sleep(5)
            GPIO.output(changePin, GPIO.HIGH)
            message = 'Reset ' + deviceName + '.'
        # For each pin, read the pin state and store it in the pins dictionary
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        templateData = {
                        'message' : message,
                        'pins' : pins
                        }
        return render_template('index.html', **templateData)

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=80)