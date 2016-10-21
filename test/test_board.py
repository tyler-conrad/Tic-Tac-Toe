from math import sqrt

from common.model.board import blank, to_string, check_line
from common.model.board import from_string
from common.model.board import Board
from common.model.board import Cell

board_string_list  = [
    'OOX X XOO',
    'XXOOOXXOX',
    'O O X X O XXO O ',
    'XXO XOXOXO  XOOX',
    'XXX   OO ',
    'OXX O   O',
    '         ']

x_has_next_turn_results = [
    True,
    False,
    True,
    False,
    False,
    True,
    True]

symbols_in_turn_order_results = [
    ('X', 'O'),
    ('O', 'X'),
    ('X', 'O'),
    ('O', 'X'),
    ('O', 'X'),
    ('X', 'O'),
    ('X', 'O'),]

is_leaf_and_score_results = [
    (True, 1.0),
    (True, 0.0),
    (False, None),
    (True, 1.0),
    (True, 1.0),
    (True, 1.0),
    (False, None)]

is_draw_results = [
    False,
    True,
    False,
    False,
    False,
    False,
    False]

def test_blank():
    for side_len in range(8):
        assert all([cell.state == ' ' for cell in blank(side_len).state])

def test_from_string():
    assert all([board_string == ''.join([
        cell.state for cell in from_string(board_string).state])
        for board_string in board_string_list])

def test_to_string():
    assert all([board_string == to_string(Board(
            [Cell(i, state) for i, state in enumerate(board_string)]))
        for board_string in board_string_list])

def test_to_from_string():
    assert all([board_string == to_string(from_string(board_string))
        for board_string in board_string_list])

def test_check_line():
    pass_list = [
        'XXX',
        'OOO',
        'XXXX',
        'XXXXXXXX',
        'OOOOO']
    assert all([check_line(line) for line in pass_list])

    fail_list = [
        'XOX',
        'XXXO',
        'XOXOXO'
        '        ',
        ' X O X X',
        '   XXXXX']
    assert not any([check_line(line) for line in fail_list])

def test_size():
    assert all([len(board_string) == from_string(board_string).size()
        for board_string in board_string_list])

def test_side_len():
    assert all([int(sqrt(len(board_string))) == from_string(board_string).side_len()
        for board_string in board_string_list])

def test_x_has_next_turn():
    assert all([result == from_string(board_string).x_has_next_turn()
        for board_string, result in zip(board_string_list, x_has_next_turn_results)])

def test_symbols_in_turn_order():
    assert all([result == from_string(board_string).symbols_in_turn_order()
        for board_string, result in zip(board_string_list, symbols_in_turn_order_results)])

def test_children():
    child_strings_by_board = [[to_string(child) for child in from_string(board_string).children()]
        for board_string in board_string_list]

    child_string_list = child_strings_by_board[0]
    assert 'OOXXX XOO' in child_string_list
    assert 'OOX XXXOO' in child_string_list

    child_string_list = child_strings_by_board[1]
    assert child_string_list == []

    child_string_list = child_strings_by_board[2]
    assert 'OXO X X O XXO O ' in child_string_list
    assert 'O OXX X O XXO O ' in child_string_list
    assert 'O O XXX O XXO O ' in child_string_list
    assert 'O O X XXO XXO O ' in child_string_list
    assert 'O O X X OXXXO O ' in child_string_list
    assert 'O O X X O XXOXO ' in child_string_list
    assert 'O O X X O XXO OX' in child_string_list

    child_string_list = child_strings_by_board[3]
    assert 'XXOOXOXOXO  XOOX' in child_string_list
    assert 'XXO XOXOXOO XOOX' in child_string_list
    assert 'XXO XOXOXO OXOOX' in child_string_list

    child_string_list = child_strings_by_board[4]
    assert 'XXXO  OO ' in child_string_list
    assert 'XXX O OO ' in child_string_list
    assert 'XXX  OOO ' in child_string_list

    child_string_list = child_strings_by_board[5]
    assert 'OXXXO   O' in child_string_list
    assert 'OXX OX  O' in child_string_list
    assert 'OXX O X O' in child_string_list
    assert 'OXX O  XO' in child_string_list

    child_string_list = child_strings_by_board[6]
    assert 'X        ' in child_string_list
    assert ' X       ' in child_string_list
    assert '  X      ' in child_string_list
    assert '   X     ' in child_string_list
    assert '    X    ' in child_string_list
    assert '     X   ' in child_string_list
    assert '      X  ' in child_string_list
    assert '       X ' in child_string_list
    assert '        X' in child_string_list

def test_is_leaf_and_score():
    assert all([result == from_string(board_string).is_leaf_and_score()
        for board_string, result in zip(
            board_string_list, is_leaf_and_score_results)])

def test_is_draw():
    assert all([result == from_string(board_string).is_draw()
        for board_string, result in zip(
            board_string_list, is_draw_results)])

def test_row_lines():
    rows = [
        'OOX',
        ' X ',
        'XOO',]
    assert all([row in from_string(board_string_list[0]).row_lines() for row in rows])

    rows = [
        'XXO',
        'OOX',
        'XOX']
    assert all([row in from_string(board_string_list[1]).row_lines() for row in rows])

    rows = [
        'O O ',
        'X X ',
        'O XX',
        'O O ']
    assert all([row in from_string(board_string_list[2]).row_lines() for row in rows])

    rows = [
        'XXO ',
        'XOXO',
        'XO  ',
        'XOOX']
    assert all([row in from_string(board_string_list[3]).row_lines() for row in rows])

    rows = [
        'XXX',
        '   ',
        'OO ']
    assert all([row in from_string(board_string_list[4]).row_lines() for row in rows])

    rows = [
        'OXX',
        ' O ',
        '  O']
    assert all([row in from_string(board_string_list[5]).row_lines() for row in rows])

    rows = [
        '   ',
        '   ',
        '   ']
    assert all([row in from_string(board_string_list[6]).row_lines() for row in rows])

def test_col_lines():
    cols = [
        'O X',
        'OXO',
        'X O']
    assert all([col in from_string(board_string_list[0]).col_lines() for col in cols])

    cols = [
        'XOX',
        'XOO',
        'OXX']
    assert all([col in from_string(board_string_list[1]).col_lines() for col in cols])

    cols = [
        'OXOO',
        '    ',
        'OXXO',
        '  X ']
    assert all([col in from_string(board_string_list[2]).col_lines() for col in cols])

    cols = [
        'XXXX',
        'XOOO',
        'OX O',
        ' O X']
    assert all([col in from_string(board_string_list[3]).col_lines() for col in cols])

    cols = [
        'X O',
        'X O',
        'X  ']
    assert all([col in from_string(board_string_list[4]).col_lines() for col in cols])

    cols = [
        'O  ',
        'XO ',
        'X O']
    assert all([col in from_string(board_string_list[5]).col_lines() for col in cols])

    cols = [
        '   ',
        '   ',
        '   ']
    assert all([col in from_string(board_string_list[6]).col_lines() for col in cols])

def test_zig_line():
    assert 'OXO' == from_string(board_string_list[0]).zig_line()[0]
    assert 'XOX' == from_string(board_string_list[1]).zig_line()[0]
    assert 'O X ' == from_string(board_string_list[2]).zig_line()[0]
    assert 'XO X' == from_string(board_string_list[3]).zig_line()[0]
    assert 'X  ' == from_string(board_string_list[4]).zig_line()[0]
    assert 'OOO' == from_string(board_string_list[5]).zig_line()[0]
    assert '   ' == from_string(board_string_list[6]).zig_line()[0]

def test_zag_line():
    assert 'XXX' == from_string(board_string_list[0]).zag_line()[0]
    assert 'XOO' == from_string(board_string_list[1]).zag_line()[0]
    assert 'O X ' == from_string(board_string_list[2]).zag_line()[0]
    assert 'XOX ' == from_string(board_string_list[3]).zag_line()[0]
    assert 'O X' == from_string(board_string_list[4]).zag_line()[0]
    assert ' OX' == from_string(board_string_list[5]).zag_line()[0]
    assert '   ' == from_string(board_string_list[6]).zag_line()[0]
