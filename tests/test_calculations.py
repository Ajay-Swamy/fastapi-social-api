from app.calculations import add
import pytest

@pytest.mark.parametrize("num1,num2,expected",[
        (3,2,5),
        (5,9,14),
        (11,12,23)
])
def test_add(num1,num2,expected):
    print("test added successfully")
    sum=add(num1,num2)
    assert sum==expected

