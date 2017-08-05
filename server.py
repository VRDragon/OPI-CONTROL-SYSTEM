import pyA20.gpio as gpio
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
import time

def create_app(configfile='server.cfg'):
    app = Flask(__name__)
    AppConfig(app, configfile)
    app.debug = app.config['DEBUG']
    Bootstrap(app)
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    # Grab all pins from the configuration file
    pins = app.config['PINS']
    # Set each pin as an output and make it low
    for pin in pins:
        gpio.setup(pin, gpio.OUT)
        gpio.output(pin, gpio.LOW)

    @app.route('/')
    def index():
        # For each pin, read the pin state and store it in the pins dictionary
        for pin in pins:
            pins[pin]['state'] = gpio.input(pin)
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
                gpio.output(pin, gpio.HIGH)
            message = 'Turned all interfaces on.'
        if master == 'off':
            # Set all pins to low
            for pin in pins:
                gpio.output(pin, gpio.LOW)
            message = 'Turned all interfaces off.'
        # For each pin, read the pin state and store it in the pins dictionary
        for pin in pins:
            pins[pin]['state'] = gpio.input(pin)
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
            gpio.output(changePin, gpio.HIGH)
            # Save the status message to be passed into the template
            message = 'Turned ' + deviceName + ' on.'
        if action == 'off':
            gpio.output(changePin, gpio.LOW)
            message = 'Turned ' + deviceName + ' off.'
        if action == 'toggle':
            # Read the pin and set it to whatever it isn't (that is, toggle it)
            gpio.output(changePin, not gpio.input(changePin))
            message = 'Toggled ' + deviceName + '.'
        if action == 'reset':
            # Set the pin to low and after 5 s back to high
            gpio.output(changePin, gpio.LOW)
            time.sleep(5)
            gpio.output(changePin, gpio.HIGH)
            message = 'Reset ' + deviceName + '.'
        # For each pin, read the pin state and store it in the pins dictionary
        for pin in pins:
            pins[pin]['state'] = gpio.input(pin)
        templateData = {
                        'message' : message,
                        'pins' : pins
                        }
        return render_template('index.html', **templateData)

    return app

if __name__ == '__main__':
    create_app().run(host='www.forledshow.sk', port=80)