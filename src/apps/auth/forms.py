"""
MiloApps - Formularios de Autenticación
Formularios WTF para login, registro, recuperación y configuración
"""

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, EmailField, BooleanField, 
                    SelectField, TextAreaField, TelField, SubmitField, HiddenField)
from wtforms.validators import (DataRequired, Email, Length, EqualTo, 
                               ValidationError, Optional, Regexp)
from wtforms.widgets import PasswordInput
from models import User, Role

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    email = EmailField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingresa un email válido')
    ], render_kw={'placeholder': 'tu@email.com', 'class': 'form-control'})
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    two_factor_token = StringField('Código 2FA (si está habilitado)', validators=[
        Optional(),
        Length(min=6, max=6, message='El código debe tener 6 dígitos'),
        Regexp(r'^\d{6}$', message='El código debe contener solo números')
    ], render_kw={'placeholder': '123456', 'class': 'form-control'})
    
    remember_me = BooleanField('Recordarme', render_kw={'class': 'form-check-input'})
    
    submit = SubmitField('Iniciar Sesión', render_kw={'class': 'btn btn-primary w-100'})

class RegisterForm(FlaskForm):
    """Formulario de registro de usuario"""
    # Información básica
    first_name = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')
    ], render_kw={'placeholder': 'Juan', 'class': 'form-control'})
    
    last_name = StringField('Apellido', validators=[
        DataRequired(message='El apellido es requerido'),
        Length(min=2, max=50, message='El apellido debe tener entre 2 y 50 caracteres')
    ], render_kw={'placeholder': 'Pérez', 'class': 'form-control'})
    
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message='El nombre de usuario es requerido'),
        Length(min=3, max=80, message='El nombre de usuario debe tener entre 3 y 80 caracteres'),
        Regexp(r'^[a-zA-Z0-9_.-]+$', message='Solo se permiten letras, números, guiones y puntos')
    ], render_kw={'placeholder': 'juan.perez', 'class': 'form-control'})
    
    email = EmailField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingresa un email válido'),
        Length(max=120, message='El email no puede superar los 120 caracteres')
    ], render_kw={'placeholder': 'juan@empresa.com', 'class': 'form-control'})
    
    # Información adicional
    phone = TelField('Teléfono', validators=[
        Optional(),
        Length(max=20, message='El teléfono no puede superar los 20 caracteres')
    ], render_kw={'placeholder': '+34 123 456 789', 'class': 'form-control'})
    
    company = StringField('Empresa', validators=[
        Optional(),
        Length(max=100, message='La empresa no puede superar los 100 caracteres')
    ], render_kw={'placeholder': 'Mi Empresa S.L.', 'class': 'form-control'})
    
    department = StringField('Departamento', validators=[
        Optional(),
        Length(max=100, message='El departamento no puede superar los 100 caracteres')
    ], render_kw={'placeholder': 'IT / Desarrollo', 'class': 'form-control'})
    
    # Contraseña
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida'),
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message='La contraseña debe contener al menos una mayúscula, una minúscula y un número')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    password2 = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message='Confirma tu contraseña'),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    # Rol (solo para admins)
    role = SelectField('Rol', coerce=int, validators=[Optional()], 
                      render_kw={'class': 'form-select'})
    
    # Términos y condiciones
    accept_terms = BooleanField('Acepto los términos y condiciones', validators=[
        DataRequired(message='Debes aceptar los términos y condiciones')
    ], render_kw={'class': 'form-check-input'})
    
    submit = SubmitField('Registrarse', render_kw={'class': 'btn btn-success w-100'})
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Cargar roles disponibles
        self.role.choices = [(r.id, r.display_name) for r in Role.query.filter_by(is_active=True).all()]
        if not self.role.choices:
            self.role.choices = [('', 'Sin roles disponibles')]
    
    def validate_username(self, username):
        """Validar que el username sea único"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso. Elige otro.')
    
    def validate_email(self, email):
        """Validar que el email sea único"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email ya está registrado. ¿Olvidaste tu contraseña?')

class ForgotPasswordForm(FlaskForm):
    """Formulario de recuperación de contraseña"""
    email = EmailField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingresa un email válido')
    ], render_kw={'placeholder': 'tu@email.com', 'class': 'form-control'})
    
    submit = SubmitField('Enviar enlace de recuperación', 
                        render_kw={'class': 'btn btn-warning w-100'})
    
    def validate_email(self, email):
        """Validar que el email exista en el sistema"""
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No existe una cuenta con este email.')

class ResetPasswordForm(FlaskForm):
    """Formulario de restablecimiento de contraseña"""
    password = PasswordField('Nueva contraseña', validators=[
        DataRequired(message='La contraseña es requerida'),
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message='La contraseña debe contener al menos una mayúscula, una minúscula y un número')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    password2 = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message='Confirma tu contraseña'),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    submit = SubmitField('Cambiar contraseña', render_kw={'class': 'btn btn-success w-100'})

class ChangePasswordForm(FlaskForm):
    """Formulario de cambio de contraseña (usuario logueado)"""
    current_password = PasswordField('Contraseña actual', validators=[
        DataRequired(message='La contraseña actual es requerida')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    new_password = PasswordField('Nueva contraseña', validators=[
        DataRequired(message='La nueva contraseña es requerida'),
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message='La contraseña debe contener al menos una mayúscula, una minúscula y un número')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    confirm_password = PasswordField('Confirmar nueva contraseña', validators=[
        DataRequired(message='Confirma tu nueva contraseña'),
        EqualTo('new_password', message='Las contraseñas deben coincidir')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    submit = SubmitField('Cambiar contraseña', render_kw={'class': 'btn btn-primary'})

class ProfileForm(FlaskForm):
    """Formulario de edición de perfil"""
    first_name = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')
    ], render_kw={'class': 'form-control'})
    
    last_name = StringField('Apellido', validators=[
        DataRequired(message='El apellido es requerido'),
        Length(min=2, max=50, message='El apellido debe tener entre 2 y 50 caracteres')
    ], render_kw={'class': 'form-control'})
    
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message='El nombre de usuario es requerido'),
        Length(min=3, max=80, message='El nombre de usuario debe tener entre 3 y 80 caracteres'),
        Regexp(r'^[a-zA-Z0-9_.-]+$', message='Solo se permiten letras, números, guiones y puntos')
    ], render_kw={'class': 'form-control'})
    
    email = EmailField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingresa un email válido'),
        Length(max=120, message='El email no puede superar los 120 caracteres')
    ], render_kw={'class': 'form-control'})
    
    phone = TelField('Teléfono', validators=[
        Optional(),
        Length(max=20, message='El teléfono no puede superar los 20 caracteres')
    ], render_kw={'class': 'form-control'})
    
    company = StringField('Empresa', validators=[
        Optional(),
        Length(max=100, message='La empresa no puede superar los 100 caracteres')
    ], render_kw={'class': 'form-control'})
    
    department = StringField('Departamento', validators=[
        Optional(),
        Length(max=100, message='El departamento no puede superar los 100 caracteres')
    ], render_kw={'class': 'form-control'})
    
    bio = TextAreaField('Biografía', validators=[
        Optional(),
        Length(max=500, message='La biografía no puede superar los 500 caracteres')
    ], render_kw={'class': 'form-control', 'rows': '3', 'placeholder': 'Cuéntanos un poco sobre ti...'})
    
    submit = SubmitField('Actualizar perfil', render_kw={'class': 'btn btn-primary'})
    
    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        """Validar que el username sea único (excepto el actual)"""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Este nombre de usuario ya está en uso. Elige otro.')
    
    def validate_email(self, email):
        """Validar que el email sea único (excepto el actual)"""
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Este email ya está registrado.')

class TwoFactorSetupForm(FlaskForm):
    """Formulario para configurar autenticación de dos factores"""
    token = StringField('Código de verificación', validators=[
        DataRequired(message='El código es requerido'),
        Length(min=6, max=6, message='El código debe tener 6 dígitos'),
        Regexp(r'^\d{6}$', message='El código debe contener solo números')
    ], render_kw={'placeholder': '123456', 'class': 'form-control text-center'})
    
    submit = SubmitField('Verificar y activar 2FA', render_kw={'class': 'btn btn-success'})

class TwoFactorDisableForm(FlaskForm):
    """Formulario para desactivar autenticación de dos factores"""
    password = PasswordField('Contraseña actual', validators=[
        DataRequired(message='La contraseña es requerida para desactivar 2FA')
    ], render_kw={'placeholder': '••••••••', 'class': 'form-control'})
    
    submit = SubmitField('Desactivar 2FA', render_kw={'class': 'btn btn-danger'})

class UserManagementForm(FlaskForm):
    """Formulario para gestión de usuarios (solo admins)"""
    user_id = HiddenField('User ID')
    
    first_name = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')
    ], render_kw={'class': 'form-control'})
    
    last_name = StringField('Apellido', validators=[
        DataRequired(message='El apellido es requerido'),
        Length(min=2, max=50, message='El apellido debe tener entre 2 y 50 caracteres')
    ], render_kw={'class': 'form-control'})
    
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message='El nombre de usuario es requerido'),
        Length(min=3, max=80, message='El nombre de usuario debe tener entre 3 y 80 caracteres')
    ], render_kw={'class': 'form-control'})
    
    email = EmailField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingresa un email válido')
    ], render_kw={'class': 'form-control'})
    
    role = SelectField('Rol', coerce=int, validators=[DataRequired()], 
                      render_kw={'class': 'form-select'})
    
    is_active = BooleanField('Usuario activo', render_kw={'class': 'form-check-input'})
    is_verified = BooleanField('Cuenta verificada', render_kw={'class': 'form-check-input'})
    
    # Campos opcionales
    phone = TelField('Teléfono', validators=[Optional()], 
                    render_kw={'class': 'form-control'})
    company = StringField('Empresa', validators=[Optional()], 
                         render_kw={'class': 'form-control'})
    department = StringField('Departamento', validators=[Optional()], 
                            render_kw={'class': 'form-control'})
    
    # Acciones
    reset_password = BooleanField('Generar nueva contraseña', 
                                 render_kw={'class': 'form-check-input'})
    unlock_account = BooleanField('Desbloquear cuenta', 
                                 render_kw={'class': 'form-check-input'})
    disable_2fa = BooleanField('Desactivar 2FA', 
                              render_kw={'class': 'form-check-input'})
    
    submit = SubmitField('Actualizar usuario', render_kw={'class': 'btn btn-primary'})
    
    def __init__(self, *args, **kwargs):
        super(UserManagementForm, self).__init__(*args, **kwargs)
        # Cargar roles disponibles
        self.role.choices = [(r.id, r.display_name) for r in Role.query.filter_by(is_active=True).all()]

class SearchForm(FlaskForm):
    """Formulario de búsqueda general"""
    query = StringField('Buscar', validators=[Optional()], 
                       render_kw={'placeholder': 'Buscar usuarios, emails...', 
                                'class': 'form-control'})
    
    submit = SubmitField('Buscar', render_kw={'class': 'btn btn-outline-primary'})

# Formularios adicionales para casos específicos
class BulkActionForm(FlaskForm):
    """Formulario para acciones en lote"""
    action = SelectField('Acción', choices=[
        ('', 'Seleccionar acción...'),
        ('activate', 'Activar usuarios'),
        ('deactivate', 'Desactivar usuarios'),
        ('delete', 'Eliminar usuarios'),
        ('export', 'Exportar datos')
    ], render_kw={'class': 'form-select'})
    
    submit = SubmitField('Ejecutar', render_kw={'class': 'btn btn-warning'})

class ImportUsersForm(FlaskForm):
    """Formulario para importar usuarios desde CSV"""
    file = StringField('Archivo CSV', render_kw={'type': 'file', 'accept': '.csv', 'class': 'form-control'})
    default_role = SelectField('Rol por defecto', coerce=int, 
                              render_kw={'class': 'form-select'})
    send_welcome_email = BooleanField('Enviar email de bienvenida', 
                                     render_kw={'class': 'form-check-input'})
    
    submit = SubmitField('Importar usuarios', render_kw={'class': 'btn btn-success'})
    
    def __init__(self, *args, **kwargs):
        super(ImportUsersForm, self).__init__(*args, **kwargs)
        self.default_role.choices = [(r.id, r.display_name) for r in Role.query.filter_by(is_active=True).all()]
