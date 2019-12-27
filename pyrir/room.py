'''
Room Class for Simulating Room Impulse Response

author: github.com/ludlows
2019-11 

This program is designed with the hope that it will be useful, but WITHOUT ANY GUARANTEE.
'''
import numbers
import numpy as np
from .microphone import Microphone
from .speaker import Speaker

class Room:
    """
    Room class
    """
    _room_id = 0
    def __init__(self, size, name=None):
        """
        Args: 
            size (meter):  (size_x, size_y, size_z) numerical tuple with length of 3
                            size_x (meter): Room Length along X Axis
                            size_y (meter): Room Length along Y Axis
                            size_z (meter): Room Length along Z Axis
            name        : str
        """
        if len(size) != 3:
            raise ValueError('The length of Room Size should be 3 !!!')
        if not all([isinstance(v, numbers.Number) for v in size]):
            raise ValueError('All the elements of Room Size should be numeric!!!')
        self._size_x, self._size_y , self._size_z = size
        if not name:
            self._name = "Room_{:d}".format(self._room_id)
        else:
            self._name = name
        self._room_id += 1
        self._mics = None 
        self._speakers = None 

    def _check_pos(self, obj_with_pos):
        """
        Returns True if the position of obj_with_pos fits with the Room Size
        Args:
            obj_with_pos: Microphone or Speaker 
        """ 
        x, y, z = obj_with_pos.get_pos()
        if x < 0 or x > self._size_x or y < 0 or y > self._size_y or z < 0 or z > self._size_z:
            return False
        return True

    def setup_mic_speaker(self, mic_or_mics, speaker_or_speakers):
        """
        Args:
            mics    : Microphone object or list of Microphones
            speakers: Speaker object or list of Speakers

        """
        # setup mic and check types
        if isinstance(mic_or_mics, Microphone):
            self._mics = (mic_or_mics,)
        elif isinstance(mic_or_mics, list) or isinstance(mic_or_mics, tuple):
            mics = list(mic_or_mics)
            if any([not isinstance(mic, Microphone) for mic in mics]):
                raise ValueError('Some Objects are not Microphone Objects')
            if any([not self._check_pos(obj) for obj in mics]):
                raise ValueError('Some Microphone Positions are not compatible with the Rooom Size')
            self._mics = tuple(mics)
        else:
            raise ValueError('The mic_or_mics value should be Microphone object or list of Microphone Objects')

        # setup speakers and check types
        if isinstance(speaker_or_speakers, Speaker):
            self._speakers = (speaker_or_speakers,)
        elif isinstance(speaker_or_speakers, list) or isinstance(speaker_or_speakers, tuple):
            spks = list(speaker_or_speakers)
            if any([not isinstance(spk, Speaker) for spk in spks]):
                raise ValueError('Some Objects are not Spkeaker Objects')
            if any([not self._check_pos(obj) for obj in spks]):
                raise ValueError('Some Speaker Positions are not compatible with the Rooom Size')
            self._speakers = tuple(spks)
        else:
            raise ValueError('The speaker_or_speakers value should be Speaker object or list of Speaker Objects')


    def mic_speaker_combination(self):
        """
        Returns list of tuples like ((mic1, mic2, ...), speaker)
        """
        if (not self._mics) or (not self._speakers):
            raise RuntimeError("The Microphones and Speakers are not setup yet.")
        comb = []
        for spk in self._speakers:
            comb.append((tuple(self._mics), spk))
        return comb
        
    def __str__(self):
        return "{}_x_{:.1f}_y_{:.1f}_z_{:.1f}".format(self._name, self._size_x, self._size_y, self._size_z)

       


class ReverbRoom(Room):
    """
    Reverb Time Room class (Defined by T60) 
    """
    pass 

class ReflectRoom(Room):
    """
    Reflection Coefficient Room class (Defined by Beta)
    """
    pass
