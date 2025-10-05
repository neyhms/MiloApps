# MiloSign App - Formularios
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError


class DocumentUploadForm(FlaskForm):
    """Formulario para subir documentos"""
    title = StringField('Título del documento', 
                       validators=[DataRequired(), Length(min=1, max=200)])
    description = TextAreaField('Descripción', 
                               validators=[Length(max=1000)])
    file = FileField('Archivo', 
                    validators=[
                        FileRequired(), 
                        FileAllowed(['pdf', 'doc', 'docx'], 
                                  'Solo archivos PDF, DOC y DOCX')
                    ])
    
    expires_in_days = SelectField('Expira en', 
                                 choices=[
                                     ('7', '7 días'),
                                     ('15', '15 días'),
                                     ('30', '30 días'),
                                     ('60', '60 días'),
                                     ('90', '90 días'),
                                     ('0', 'Sin expiración')
                                 ], default='30')
    
    requires_all_signatures = BooleanField('Requiere todas las firmas', 
                                         default=True)
    signature_order = BooleanField('Orden específico de firma')


class AddSignerForm(FlaskForm):
    """Formulario para agregar firmantes"""
    email = StringField('Email del firmante',
                       validators=[DataRequired(), Email()])
    name = StringField('Nombre completo',
                      validators=[DataRequired(), Length(min=1, max=100)])
    order_index = SelectField('Orden de firma', 
                             choices=[(str(i), f'Posición {i}') for i in range(1, 11)],
                             default='1')
    notes = TextAreaField('Notas para el firmante',
                         validators=[Length(max=500)])


class SignatureForm(FlaskForm):
    """Formulario para firmar documento"""
    signature_data = HiddenField('Datos de firma', validators=[DataRequired()])
    agree_terms = BooleanField('Acepto los términos y condiciones',
                              validators=[DataRequired()])
    notes = TextAreaField('Notas adicionales',
                         validators=[Length(max=500)])


class DocumentSearchForm(FlaskForm):
    """Formulario para buscar documentos"""
    query = StringField('Buscar documentos')
    status = SelectField('Estado',
                        choices=[
                            ('', 'Todos'),
                            ('draft', 'Borrador'),
                            ('pending', 'Pendiente'),
                            ('signed', 'Firmado'),
                            ('cancelled', 'Cancelado'),
                            ('expired', 'Expirado')
                        ])
    sort_by = SelectField('Ordenar por',
                         choices=[
                             ('created_at', 'Fecha de creación'),
                             ('title', 'Título'),
                             ('status', 'Estado'),
                             ('updated_at', 'Última actualización')
                         ], default='created_at')


class TemplateForm(FlaskForm):
    """Formulario para plantillas de documentos"""
    name = StringField('Nombre de la plantilla',
                      validators=[DataRequired(), Length(min=1, max=200)])
    description = TextAreaField('Descripción',
                               validators=[Length(max=1000)])
    template_file = FileField('Archivo de plantilla',
                             validators=[
                                 FileRequired(),
                                 FileAllowed(['pdf', 'doc', 'docx'],
                                           'Solo archivos PDF, DOC y DOCX')
                             ])
    
    default_expiration_days = SelectField('Expiración por defecto',
                                         choices=[
                                             ('7', '7 días'),
                                             ('15', '15 días'),
                                             ('30', '30 días'),
                                             ('60', '60 días'),
                                             ('90', '90 días'),
                                             ('0', 'Sin expiración')
                                         ], default='30')
    
    requires_all_signatures = BooleanField('Requiere todas las firmas por defecto',
                                         default=True)
    signature_order = BooleanField('Orden específico de firma por defecto')
    is_public = BooleanField('Plantilla pública')


class BulkActionForm(FlaskForm):
    """Formulario para acciones en lote"""
    action = SelectField('Acción',
                        choices=[
                            ('', 'Seleccionar acción...'),
                            ('cancel', 'Cancelar documentos'),
                            ('resend', 'Reenviar notificaciones'),
                            ('extend', 'Extender expiración'),
                            ('delete', 'Eliminar documentos')
                        ])
    confirm = BooleanField('Confirmo que quiero realizar esta acción')
    
    def validate_action(self, field):
        if not field.data:
            raise ValidationError('Debes seleccionar una acción.')
    
    def validate_confirm(self, field):
        if not field.data:
            raise ValidationError('Debes confirmar la acción.')


class SignatureSettingsForm(FlaskForm):
    """Formulario para configuración de firmas"""
    signature_type = SelectField('Tipo de firma por defecto',
                                choices=[
                                    ('digital', 'Firma digital'),
                                    ('drawn', 'Firma dibujada'),
                                    ('typed', 'Firma escrita'),
                                    ('upload', 'Subir imagen')
                                ], default='digital')
    
    require_password = BooleanField('Requiere contraseña para firmar')
    save_signature = BooleanField('Guardar firma para uso futuro')
    
    # Configuración de notificaciones
    notify_on_sign = BooleanField('Notificar cuando alguien firma', default=True)
    notify_on_complete = BooleanField('Notificar cuando se complete', default=True)
    notify_on_expire = BooleanField('Notificar antes de expirar', default=True)
    
    reminder_days = SelectField('Recordar cada',
                               choices=[
                                   ('1', '1 día'),
                                   ('3', '3 días'),
                                   ('7', '7 días'),
                                   ('0', 'No enviar recordatorios')
                               ], default='3')