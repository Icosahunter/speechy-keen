
from PyQt5.QtCore import pyqtSignal, QObject
from enum import Enum
from ..app import data
import json

class SpeechNotesData(QObject):
    """ """

    def __init__(self):
        """ The constructor """

        super().__init__()

        self._notes = {
            'transcript' : {},
            'prompts' : {}
        }

    def set_author(self, author):
        self._notes['author'] = author

    def set_speech_name(self, name):
        self._notes['speech_name'] = name

    def author(self):
        return self._notes['author']

    def speech_name(self):
        return self._notes['speech_name']

    def from_plain_text(self, prompt_text, transcript_text):
        """ Sets the prompts and transcript from plain text """

        self._notes['transcript'] = self.parse_paragraphs(transcript_text)
        self._notes['prompts'] = self.parse_paragraphs(prompt_text)

    def from_dictionary(self, notes_dict):
        self._notes = notes_dict

    def transcript(self):
        return self.unparse_paragraphs(self._notes['transcript'])

    def prompts(self):
        return self.unparse_paragraphs(self._notes['prompts'])
    
    def prompt_at(self, index):
        ind = list(self._notes['prompts'])[index]
        return self._notes['prompts'][ind]

    def prompt_count(self):
        return len(self._notes['prompts'])

    def transcript_at(self, index):
        ind = list(self._notes['transcript'])[index]
        return self._notes['transcript'][ind]

    def transcript_count(self):
        return len(self._notes['transcript'])

    def unparse_paragraphs(self, par_dict):
        return '\n\n'.join([f'{k}) {v}' for k, v in par_dict.items()])

    def parse_paragraphs(self, mystring):
        """ 
            Parse a string into a list of paragraphs

            The paragraphs will be indexed by numbers present in
            the text when they are of the form 'n)'
        """
        pars = mystring.split('\n\n')  #split into paragraphs
        pars = {x.split(')')[0] : ')'.join(x.split(')')[1:]).strip() for x in pars}
        return pars

    def save_to_file(self):
        data.store_data('documents/speech_notes/' + self._notes['speech_name'], self._notes)