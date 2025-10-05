# MiloSign App - Modelos de datos
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.models import db
from datetime import datetime


class Document(db.Model):
    """Modelo para documentos a firmar"""

    __tablename__ = "milosign_documents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(500), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    file_hash = db.Column(db.String(64), nullable=True)  # SHA-256
    file_size = db.Column(db.Integer, nullable=True)

    # Estados: draft, pending, signed, cancelled, expired
    status = db.Column(db.String(20), nullable=False, default="draft")

    # Relaciones
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", backref="owned_documents", foreign_keys=[owner_id])

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    expires_at = db.Column(db.DateTime, nullable=True)

    # Configuración de firma
    requires_all_signatures = db.Column(db.Boolean, default=True)
    signature_order = db.Column(db.Boolean, default=False)  # Orden específico

    # Relaciones
    signatures = db.relationship(
        "Signature", backref="document", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Document {self.title}>"

    def get_signature_progress(self):
        """Obtener progreso de firmas"""
        total = len(self.signatures)
        signed = len([s for s in self.signatures if s.status == "signed"])
        return {
            "signed": signed,
            "total": total,
            "percentage": (signed / total) * 100 if total > 0 else 0,
        }

    def is_fully_signed(self):
        """Verificar si está completamente firmado"""
        if not self.signatures:
            return False
        return all(sig.status == "signed" for sig in self.signatures)

    def can_be_signed_by(self, user):
        """Verificar si un usuario puede firmar este documento"""
        signature = next((s for s in self.signatures if s.signer_id == user.id), None)
        return signature and signature.status == "pending"


class Signature(db.Model):
    """Modelo para firmas de documentos"""

    __tablename__ = "milosign_signatures"

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(
        db.Integer, db.ForeignKey("milosign_documents.id"), nullable=False
    )
    signer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    signer = db.relationship("User", backref="signatures")

    # Estados: pending, signed, declined, expired
    status = db.Column(db.String(20), nullable=False, default="pending")

    # Datos de la firma
    signature_data = db.Column(db.Text, nullable=True)  # Base64 de la firma
    signature_type = db.Column(
        db.String(20), default="digital"
    )  # digital, biometric, etc.

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    signed_at = db.Column(db.DateTime, nullable=True)

    # Información de auditoría
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)

    # Orden de firma (si se requiere orden específico)
    order_index = db.Column(db.Integer, default=0)

    # Metadatos adicionales
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Signature {self.document_id}:{self.signer_id}>"


class SignatureTemplate(db.Model):
    """Plantillas de documentos para firma"""

    __tablename__ = "milosign_templates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    template_file = db.Column(db.String(500), nullable=False)

    # Configuración por defecto
    default_expiration_days = db.Column(db.Integer, default=30)
    requires_all_signatures = db.Column(db.Boolean, default=True)
    signature_order = db.Column(db.Boolean, default=False)

    # Control de acceso
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    creator = db.relationship("User", backref="signature_templates")
    is_public = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<SignatureTemplate {self.name}>"


class SignatureAudit(db.Model):
    """Auditoría detallada de firmas"""

    __tablename__ = "milosign_audit"

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey("milosign_documents.id"))
    signature_id = db.Column(db.Integer, db.ForeignKey("milosign_signatures.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    action = db.Column(db.String(100), nullable=False)  # view, sign, decline, etc.
    details = db.Column(db.Text, nullable=True)  # JSON con detalles adicionales

    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SignatureAudit {self.action}>"
