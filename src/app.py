#!/usr/bin/python3

import pygame
from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

pygame.init()
# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.set_num_channels(3)  # Three separate channels for different sound types

# Define channels
CHANNELS = {
    'notification': pygame.mixer.Channel(0),
    'ui': pygame.mixer.Channel(1),
    'alarm': pygame.mixer.Channel(2)
}

# Default volumes (scale 0.0 to 1.0)
DEFAULT_VOLUMES = {
    'notification': 1.0,
    'ui': 0.5,  # UI sound volume remains constant
    'alarm': 1.0
}

# Set initial volume levels
for key, channel in CHANNELS.items():
    channel.set_volume(DEFAULT_VOLUMES[key])


@app.route('/play', methods=['POST'])
def play():
    data = request.json
    sound_type = data.get('sound_type')
    filename = data.get('filename')
    override = data.get('override', False)

    if sound_type not in CHANNELS or not filename:
        return jsonify({'error': 'Invalid sound type or filename'}), 400

    if CHANNELS[sound_type].get_busy():
        if override:
            CHANNELS[sound_type].stop()  # Stop current sound if override is true
        else:
            return jsonify(
                {'error': f'{sound_type.capitalize()} sound is already playing. Use "override" to force play.'}), 409

    sound = pygame.mixer.Sound(filename)
    if sound_type == 'notification':
        if CHANNELS['alarm'].get_busy():
            adjust_alarm_volume_for_notification()
        threading.Thread(target=restore_volume_after_notification, args=(sound.get_length(),)).start()

    CHANNELS[sound_type].play(sound)
    return jsonify({'message': f'Playing {sound_type} sound', 'file': filename}), 200


def adjust_alarm_volume_for_notification():
    # Reduce alarm volume when notification is played
    CHANNELS['alarm'].set_volume(0.2)


def restore_volume_after_notification(duration):
    # Wait for the notification sound to finish then restore alarm volume
    time.sleep(duration)
    CHANNELS['alarm'].set_volume(DEFAULT_VOLUMES['alarm'])


@app.route('/stop', methods=['POST'])
def stop():
    # Stop all channels and reset volumes
    for channel in CHANNELS.values():
        channel.stop()
    for key in DEFAULT_VOLUMES:
        CHANNELS[key].set_volume(DEFAULT_VOLUMES[key])
    return jsonify({'message': 'All sounds stopped'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
