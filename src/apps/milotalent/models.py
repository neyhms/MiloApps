"""
MiloTalent - Modelos de Base de Datos
Sistema de Registro de Prestadores de Servicios

Nueva estructura basada en integración con SAP y sistemas de nómina
"""

from datetime import datetime, date
from enum import Enum
import uuid

from models import db


# ========================================
# MODELOS DE CONFIGURACIÓN
# ========================================


class Municipio(db.Model):
    """
    Tabla de municipios de Colombia con departamentos
    """
    __tablename__ = "talent_municipios"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(100), nullable=False)
    codigo_dane = db.Column(db.String(10), nullable=True, unique=True)
    nombre_completo = db.Column(db.String(200), nullable=False)  # "Municipio - Departamento"
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_creacion = db.Column(db.String(36), nullable=True)

    def __repr__(self):
        return f"<Municipio {self.nombre_completo}>"
    
    @property
    def display_name(self):
        """Nombre para mostrar en dropdowns"""
        return self.nombre_completo
    
    def to_dict(self):
        """Convierte a diccionario para API"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'departamento': self.departamento,
            'codigo_dane': self.codigo_dane,
            'nombre_completo': self.nombre_completo,
            'activo': self.activo
        }


# ========================================
# ENUMS PARA LA NUEVA ESTRUCTURA
# ========================================


class Sexo(Enum):
    """Sexo del prestador"""
    M = "M"
    F = "F"


class EstadoCivil(Enum):
    """Estado civil"""
    SOLTERO = "Soltero"
    CASADO = "Casado"
    UNION_LIBRE = "Unión Libre"
    DIVORCIADO = "Divorciado"
    VIUDO = "Viudo"


class TipoCuenta(Enum):
    """Tipos de cuenta bancaria"""
    AHORROS = "02 Cuenta de Ahorros"
    CORRIENTE = "01 Cuenta Corriente"


class RegimenIVA(Enum):
    """Régimen de IVA"""
    SIMPLIFICADO = "98 RUT Régimen Simplificado"
    COMUN = "97 RUT Régimen Común"


class TipoRiesgo(Enum):
    """Tipos de riesgo ARL"""
    CLASE_I = "001 Labores administrativas Clase I"
    CLASE_II = "002 Labores operativas Clase II"
    CLASE_III = "003 Labores de riesgo medio Clase III"
    CLASE_IV = "004 Labores de alto riesgo Clase IV"
    CLASE_V = "005 Labores de máximo riesgo Clase V"


class IdentidadGenero(Enum):
    """Identidad de género"""
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"
    NO_BINARIO = "NO BINARIO"
    OTRO = "OTRO"


class Raza(Enum):
    """Clasificación racial"""
    MESTIZO = "MESTIZO"
    AFRODESCENDIENTE = "AFRODESCENDIENTE"
    INDIGENA = "INDÍGENA"
    BLANCO = "BLANCO"
    OTRO = "OTRO"


class NuevoViejo(Enum):
    """Clasificación nuevo/existente"""
    NUEVO = "N"
    VIEJO = "V"


class TipoRH(Enum):
    """Tipos de sangre RH"""
    A_POSITIVO = "A+"
    A_NEGATIVO = "A-"
    B_POSITIVO = "B+"
    B_NEGATIVO = "B-"
    AB_POSITIVO = "AB+"
    AB_NEGATIVO = "AB-"
    O_POSITIVO = "O+"
    O_NEGATIVO = "O-"


# ========================================
# MODELO PRINCIPAL: PRESTADOR DE SERVICIOS
# ========================================


class PrestadorServicio(db.Model):
    """
    Modelo de Prestador de Servicios
    Nueva estructura basada en integración SAP y sistemas de nómina
    """

    __tablename__ = "talent_prestadores_new"

    # Clave primaria
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # IDENTIFICACIÓN
    cedula_ps = db.Column(db.String(10), nullable=False, unique=True, index=True)
    expedida_id = db.Column(db.Integer, db.ForeignKey('talent_municipios.id'), nullable=False)
    
    # NOMBRES COMPLETOS
    nombre_1 = db.Column(db.String(50), nullable=False)
    nombre_2 = db.Column(db.String(50), nullable=True)
    apellido_1 = db.Column(db.String(50), nullable=False)
    apellido_2 = db.Column(db.String(50), nullable=True)
    
    # INFORMACIÓN BÁSICA
    sexo = db.Column(db.String(1), nullable=False)
    codigo_sap = db.Column(db.String(20), nullable=False, unique=True)
    
    # NACIMIENTO  
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    ciudad_nacimiento_id = db.Column(db.Integer, db.ForeignKey('talent_municipios.id'), nullable=False)
    pais_nacimiento = db.Column(db.String(100), nullable=False, default='CO')
    
    # CONTACTO Y RESIDENCIA
    direccion = db.Column(db.String(200), nullable=False)
    pais_residencia = db.Column(db.String(100), nullable=False, default='CO')
    municipio_residencia_id = db.Column(db.Integer, db.ForeignKey('talent_municipios.id'), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(120), nullable=False)
    
    # INFORMACIÓN PERSONAL
    profesion = db.Column(db.String(100), nullable=False)
    estado_civil = db.Column(db.String(15), nullable=False)
    no_hijos = db.Column(db.Integer, nullable=False, default=0)
    rh = db.Column(db.String(11), nullable=False)
    discapacidad = db.Column(db.String(100), nullable=False, default='NINGUNA')
    identidad_genero = db.Column(db.String(15), nullable=False)
    raza = db.Column(db.String(20), nullable=False)
    
    # INFORMACIÓN BANCARIA
    banco = db.Column(db.String(100), nullable=False)
    cuenta_bancaria = db.Column(db.String(50), nullable=False)
    tipo_cuenta = db.Column(db.String(15), nullable=False)
    
    # SEGURIDAD SOCIAL Y TRIBUTARIA
    regimen_iva = db.Column(db.String(15), nullable=False)
    eps = db.Column(db.String(100), nullable=False)
    afp = db.Column(db.String(100), nullable=False)
    arl = db.Column(db.String(100), nullable=False)
    tipo_riesgo = db.Column(db.String(10), nullable=False)
    caja = db.Column(db.String(100), nullable=True)
    operador_ss = db.Column(db.String(100), nullable=False)
    
    # SISTEMA
    nuevo_viejo = db.Column(db.String(5), nullable=False)
    area_personal = db.Column(db.String(50), nullable=False)
    
    # METADATA DEL SISTEMA
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_registro = db.Column(db.String(36))
    fecha_actualizacion = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # RELACIONES CON MUNICIPIOS
    expedida_municipio = db.relationship('Municipio', foreign_keys=[expedida_id], lazy='select')
    ciudad_nacimiento_municipio = db.relationship('Municipio', foreign_keys=[ciudad_nacimiento_id], lazy='select')
    municipio_residencia_municipio = db.relationship('Municipio', foreign_keys=[municipio_residencia_id], lazy='select')

    def __repr__(self):
        return f"<PrestadorServicio {self.nombre_completo} - {self.cedula_ps}>"

    @property
    def nombre_completo(self):
        """Retorna el nombre completo concatenado"""
        nombres = f"{self.nombre_1}"
        if self.nombre_2:
            nombres += f" {self.nombre_2}"
        apellidos = f"{self.apellido_1}"
        if self.apellido_2:
            apellidos += f" {self.apellido_2}"
        return f"{nombres} {apellidos}"

    @property
    def edad(self):
        """Calcula la edad actual basada en fecha de nacimiento"""
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return 0

    def to_dict(self):
        """Convierte el objeto a diccionario para serialización"""
        return {
            'id': self.id,
            'cedula_ps': self.cedula_ps,
            'nombre_completo': self.nombre_completo,
            'mail': self.mail,
            'telefono': self.telefono,
            'profesion': self.profesion,
            'edad': self.edad,
            'codigo_sap': self.codigo_sap
        }


# ========================================
# AUDITORÍA DEL SISTEMA
# ========================================


class AuditoriaPS(db.Model):
    """
    Tabla de auditoría para el sistema de PS
    """
    __tablename__ = "talent_auditoria"

    id = db.Column(db.Integer, primary_key=True)
    ps_id = db.Column(db.Integer, db.ForeignKey("talent_prestadores_new.id"))
    usuario_id = db.Column(db.String(36), nullable=False)
    accion = db.Column(db.String(50), nullable=False)
    modulo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    ip_usuario = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    valores_anteriores = db.Column(db.Text)  # JSON
    valores_nuevos = db.Column(db.Text)      # JSON

    def __repr__(self):
        return f"<AuditoriaPS {self.accion} - {self.fecha_hora}>"