from pytest import raises

from common.model.cell import Cell
from common.model.cell import InvalidMove


def test_init():
    assert Cell(0, ' ').state ==  ' '
    assert Cell(0, ' ').index ==  0

def test_set_state():
    cell = Cell(0, ' ')
    cell.set_state('X')
    assert cell.state == 'X'

    cell = Cell(0, ' ')
    cell.set_state('X')
    with raises(InvalidMove):
        cell.set_state('X')
