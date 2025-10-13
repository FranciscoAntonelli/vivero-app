from unittest import TestCase
from unittest.mock import Mock

from models.resultado_autenticacion import ResultadoAutenticacion
from use_cases.login.login_use_case import LoginUseCase

class TestLoginUseCase(TestCase):

    def test_autenticar_valor_incorrecto(self):
        # Mock del validador
        mock_validador = Mock()
        mock_validador.validar.return_value = ["Usuario vacío"]

        # Mock del servicio
        mock_service = Mock()
        mock_service.verificar_credenciales.return_value = None

        use_case = LoginUseCase(mock_service, mock_validador)
        resultado = use_case.autenticar("", "123")

        assert isinstance(resultado, ResultadoAutenticacion)
        assert not resultado.exito
        assert "Usuario vacío" in resultado.errores

    def test_autenticar_correcto(self):
        mock_validador = Mock()
        mock_validador.validar.return_value = []

        mock_usuario = Mock()
        mock_service = Mock()
        mock_service.verificar_credenciales.return_value = mock_usuario

        use_case = LoginUseCase(mock_service, mock_validador)
        resultado = use_case.autenticar("juan", "1234")

        assert resultado.exito
        assert resultado.usuario == mock_usuario