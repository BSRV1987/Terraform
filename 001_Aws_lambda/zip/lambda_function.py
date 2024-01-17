#!/usr/bin/python
# -*- coding: utf-8 -*-
import json


def lambda_handler(event, context):

    
    # Flip blocks to decode from little Endian.

    def flip_blocks(binaryString):
        str1 = binaryString[0:4]
        str2 = binaryString[4:]
        return str2[::-1] + str1[::-1]

    def state_description(id):
        desc = None
        if id == 0:
            desc = 'power off'
        elif id == 1:
            desc = 'power on'
        elif id == 2:
            desc = 'discharge'
        elif id == 3:
            desc = 'charge'
        elif id == 4:
            desc = 'charge complete'
        elif id == 5:
            desc = 'host mode'
        elif id == 6:
            desc = 'shutdown'
        elif id == 7:
            desc = 'error'
        elif id == 8:
            desc = 'undefined'
        else:
            desc = 'Invalid State'

        return desc

    hex_value = event['payload']

    num_of_bits = 64

    # zfill used for the bad boy 6188293726C75C00 :)

    binary_string = bin(int(hex_value, 16))[2:].zfill(num_of_bits)

    rev_bin = binary_string[::-1]

    # print(binary_string)

    Decoded_string = ''

    i = 0

    while i <= len(rev_bin):
        Decoded_string = Decoded_string + flip_blocks(rev_bin[i:i + 8])
        i = i + 8

    # Logic to extract data from bits. Hoping values are always available at the same place.

    time = int(Decoded_string[-36:-4], 2)

    state = state_description(int(Decoded_string[-40:-36], 2))

    state_of_charge = int(Decoded_string[-48:-40], 2) / 2

    temperature = int(Decoded_string[-56:-48], 2) / 2 - 20.0

    result_dict = {
        'time': time,
        'state': state,
        'state_of_charge': state_of_charge,
        'temperature': temperature,
        }

    json_result = json.dumps(result_dict, indent=2)

    return json_result
