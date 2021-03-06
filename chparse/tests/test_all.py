"""Test various aspects of Pages."""
from unittest import TestCase
from sys import version_info
from os import path
from io import StringIO
import chparse
from chparse.chart import Chart
from chparse.note import Note, Event, SyncEvent
from chparse.instrument import Instrument
from chparse import flags

if version_info[0] > 2:
    basestring = str # pylint: disable=invalid-name

with open(path.join(path.dirname(__file__), 'Test.chart')) as chartfile:
    # You may notice this loads the contents of a real file into a StringIO.
    # This is to prevent locking up the real file in case the script is
    # unable to close it, since never closing a StringIO isn't too bad.
    # The file in question is also small enough to be held completely in memory.
    chart = StringIO(chartfile.read())

GLOBALS = {}

class TestAll(TestCase):
    """Test everything."""

    @staticmethod
    def _load_if_not_loaded():
        if 'chartobj' not in GLOBALS:
            GLOBALS['chartobj'] = chparse.load(chart)

    def test_load(self):
        """Assert that loading a valid chart works."""
        self._load_if_not_loaded()
        self.assertTrue(isinstance(GLOBALS['chartobj'], Chart))
        self.assertTrue(GLOBALS['chartobj'].Name == 'Test')

    def test_instrument(self):
        """Assert that the ExpertSingle track is an Instrument."""
        self._load_if_not_loaded()
        self.assertTrue(isinstance(GLOBALS['chartobj'].instruments[
            flags.EXPERT
        ][flags.GUITAR], Instrument))

    def test_note(self):
        """Assert that the first note of the ExpertSingle track is a Note.
        Check flags while we're at it too.
        """
        self._load_if_not_loaded()
        notes = GLOBALS['chartobj'].instruments[flags.EXPERT][
            flags.GUITAR
        ]
        self.assertTrue(isinstance(notes[0], Note))
        self.assertTrue(notes[1].is_forced)
        self.assertTrue(notes[2].is_tap)
        self.assertTrue(notes[3].is_open)
        notes = GLOBALS['chartobj'].instruments[flags.EXPERT][
            flags.GHL_GUITAR
        ]
        self.assertTrue(isinstance(notes[0], Note))
        self.assertTrue(isinstance(notes[1], Event))
        self.assertTrue(notes[1].event == 'solo')

    def test_events(self):
        """Assert that the Events track works."""
        self._load_if_not_loaded()
        track = GLOBALS['chartobj'].instruments[flags.NA][flags.EVENTS]
        self.assertTrue(isinstance(track, Instrument))
        self.assertTrue(isinstance(track[0], Event))

    def test_sync(self):
        """Assert that the SyncTrack track works."""
        self._load_if_not_loaded()
        track = GLOBALS['chartobj'].instruments[flags.NA][flags.SYNC]
        self.assertTrue(isinstance(track, Instrument))
        self.assertTrue(isinstance(track[0], SyncEvent))
