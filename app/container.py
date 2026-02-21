from db.db import conexion

from domain.creators.venta_creator import VentaCreator
from repositories.productos_repository import ProductosRepository
from repositories.categorias_repository import CategoriasRepository
from repositories.usuarios_repository import UsuarioRepository
from repositories.meta_repository import MetaRepository
from repositories.ventas_repository import VentasRepository
from repositories.detalle_venta_repository import DetalleVentaRepository
from repositories.reportes_repository import ReportesRepository

from services.productos_service import ProductosService
from services.login_service import LoginService
from services.categorias_service import CategoriasService
from services.meta_service import MetaService
from services.venta_domain_service import VentaDomainService
from services.ventas_service import VentasService
from services.detalle_venta_service import DetalleVentaService
from services.password_hasher import PasswordHasher
from services.reportes_service import ReportesService

from use_cases.categorias.categorias_use_case import CategoriasUseCase
from use_cases.impresoras.imprimir_productos_use_case import ImprimirProductosUseCase
from use_cases.meta.productos_meta_use_case import ProductosMetaUseCase
from use_cases.ventas.ventas_query import VentasQuery
from use_cases.impresoras.imprimir_reportes_use_case import ImprimirReportesUseCase

from validators.coincidencia_contrasenia_validador import CoincidenciaContraseniaValidador
from validators.coordinador_validaciones import CoordinadorValidaciones
from validators.campos_obligatorios_validador import CamposObligatoriosValidador
from validators.longitud_maxima_validador import LongitudMaximaValidador

from utils.impresion.impresora_productos import ImpresoraProductos
from utils.impresion.impresora_reportes import ImpresoraReportes

from infrastructure.reportes.matplotlib_grafico_renderer import MatplotlibGraficoRenderer

from use_cases.auth.login_use_case import LoginUseCase
from use_cases.auth.registrar_usuario_use_case import RegistrarUsuarioUseCase
from use_cases.productos.productos_use_case import ProductosUseCase
from use_cases.productos.producto_popup_use_case import ProductoPopupUseCase
from use_cases.productos.producto_saver import ProductoSaver
from use_cases.ventas.ventas_use_case import VentaUseCase
from use_cases.reportes.reportes_use_case import ReportesUseCase

from validators.longitud_minima_validador import LongitudMinimaValidador
from validators.valor_positivo_validador import ValorPositivoValidador


def build_container():
    # Repositories
    productos_repo = ProductosRepository(conexion)
    usuario_repo = UsuarioRepository(conexion)
    categorias_repo = CategoriasRepository(conexion)
    meta_repo = MetaRepository(conexion)
    ventas_repo = VentasRepository(conexion)
    detalle_repo = DetalleVentaRepository(conexion)
    reportes_repo = ReportesRepository(conexion)

    # Services
    productos_service = ProductosService(productos_repo)
    password_hasher = PasswordHasher()
    login_service = LoginService(usuario_repo, password_hasher)
    categorias_service = CategoriasService(categorias_repo)
    meta_service = MetaService(meta_repo)
    ventas_service = VentasService(ventas_repo)
    detalle_service = DetalleVentaService(detalle_repo)
    reportes_service = ReportesService(reportes_repo)

    # Validators
    login_validator = CoordinadorValidaciones([
        CamposObligatoriosValidador({
            "usuario": "El usuario es obligatorio.",
            "password": "La contraseña es obligatoria."
        })
    ])

    registro_validadores = CoordinadorValidaciones([
        CamposObligatoriosValidador({
            "usuario": "El usuario es obligatorio.",
            "password": "La contraseña es obligatoria.",
            "password_confirm": "Debe confirmar la contraseña."
        }),
        LongitudMinimaValidador("password", 6),
        LongitudMinimaValidador("usuario", 3),
        CoincidenciaContraseniaValidador(),
    ])

    producto_validator = CoordinadorValidaciones([
        CamposObligatoriosValidador({
            "nombre": "El nombre es obligatorio.",
            "categoria": "La categoría es obligatoria.",
            "precio_unitario": "El precio es obligatorio.",
            "cantidad": "La cantidad es obligatoria."
        }),
        LongitudMaximaValidador("medida", 30),
        ValorPositivoValidador("precio_unitario", "El precio debe ser mayor a 0."),
    ])
 
    impresora_productos = ImpresoraProductos()
    impresora_reportes = ImpresoraReportes()

    saver = ProductoSaver(productos_service)

    venta_creator = VentaCreator()
    venta_domain_service = VentaDomainService(
        ventas_service=ventas_service,
        detalle_service=detalle_service,
        productos_service=productos_service
    )
    ventas_query_service = VentasQuery(
        ventas_service=ventas_service,
        detalle_service=detalle_service
    )

    # Use cases
    return {
        "login_use_case": LoginUseCase(login_service, login_validator),
        "registrar_usuario_use_case": RegistrarUsuarioUseCase(usuario_repo, password_hasher, registro_validadores),
        "productos_use_case": ProductosUseCase(
            productos_service
        ),
        "categorias_use_case": CategoriasUseCase(
            categorias_service
        ),
        "productos_meta_use_case": ProductosMetaUseCase(
            meta_service
        ),
        "imprimir_productos_use_case": ImprimirProductosUseCase(
            impresora_productos
        ),
        "imprimir_reportes_use_case": ImprimirReportesUseCase(
            reportes_service,
            impresora_reportes
        ),
        "producto_popup_use_case": ProductoPopupUseCase(
            coordinador_validaciones=producto_validator,
            saver=saver,
            categorias_service=categorias_service
        ),
        "venta_use_case": VentaUseCase(
            venta_creator,
            venta_domain_service,
            ventas_query_service
        ),
        "reportes_use_case": ReportesUseCase(
            reportes_service
        ),
        "grafico_renderer": MatplotlibGraficoRenderer()
    }