from app.calculations import add, substract, multiply, devide

def test_add():
    # print("testing adding function")
    assert add(5, 3) == 8

def test_substract():
    assert substract(9, 4) == 5


def test_multiply():
    assert multiply(1, 4) == 4


def test_devide():
    assert devide(10, 2) == 5