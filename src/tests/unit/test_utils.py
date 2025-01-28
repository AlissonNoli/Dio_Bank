import pytest
from src.utils import eleva_quadrado, requires_roles
from http import HTTPStatus

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

def test_requires_roles_success(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = 'admin'
    
    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_function = requires_roles('admin')(lambda: "success")            

    # When    
    result = decorated_function()
    
    # Then
    assert result == "success"
        
def test_requires_roles_fail(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = 'normal'
    
    mocker.patch('src.utils.get_jwt_identity'), 
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_function = requires_roles('admin')(lambda: "success")            
    
    # When
    result = decorated_function()

    # Then
    assert result == ({"msg": "Admin only!"}, HTTPStatus.FORBIDDEN)