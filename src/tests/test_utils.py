import pytest
from src.utils import eleva_quadrado

@pytest.mark.parametrize("entrada, esperado", [(2, 4), (3, 9), (4, 16), (0, 0), (-2, 4)])
def test_eleva_quadrado_sucesso(entrada, esperado):
    resultado = eleva_quadrado(entrada)
    assert resultado == esperado

@pytest.mark.parametrize("entrada, exc_class, msg", [
    ("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"), 
    (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'"),
    ([2], TypeError, "unsupported operand type(s) for ** or pow(): 'list' and 'int'"),
    ({2: 2}, TypeError, "unsupported operand type(s) for ** or pow(): 'dict' and 'int'"),
])
def test_eleva_quadrado_erro(entrada, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(entrada)
    assert str(exc.value) == msg