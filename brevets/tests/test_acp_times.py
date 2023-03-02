"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import arrow
from acp_times import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_breveterrors():
    nose.tools.assert_raises(BrevetDistERROR, open_time, 200, -1, arrow.now())
    nose.tools.assert_raises(BrevetDistERROR, open_time, 200, 1001, arrow.now())
    nose.tools.assert_raises(BrevetTypeERROR, open_time, 200, 200.0, arrow.now())

def test_controldisterror():
    nose.tools.assert_raises(ControlDistERROR, open_time, -1, 200, arrow.now())
    nose.tools.assert_raises(ControlDistERROR, open_time, 1001, 200, arrow.now())
    
def test_open_time():
    assert open_time(30, 200, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T00:53:00+00:00")
    assert open_time(200, 200, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T05:53:00+00:00")
    
    assert open_time(0, 200, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T00:00:00+00:00")

    assert open_time(300, 1000, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T09:00:00+00:00")
    assert open_time(500, 1000, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T15:28:00+00:00")
    assert open_time(700, 1000, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T22:22:00+00:00")
    assert open_time(1000, 1000, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-02T09:05:00+00:00")

def test_close_time():
    assert close_time(30, 200, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T02:30:00+00:00")
    assert close_time(200, 200, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T13:30:00+00:00")

    assert close_time(0, 200, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T01:00:00+00:00")

    assert close_time(300, 1000, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T20:00:00+00:00")
    assert close_time(500, 1000, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-02T09:20:00+00:00")
    assert close_time(700, 1000, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-03T00:45:00+00:00")
    assert close_time(1000, 1000, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-04T03:00:00+00:00")

def test_open_close_times_floats():
     assert open_time(50.6, 200, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T01:30:00+00:00")
     assert close_time(50.6, 200, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T03:33:00+00:00")

     assert open_time(300.2, 300, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T09:00:00+00:00")
     assert close_time(300.2, 300, arrow.get("2023-01-01T00:00:00+00:00")) == arrow.get("2023-01-01T20:00:00+00:00")