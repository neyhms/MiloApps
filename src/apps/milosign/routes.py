# MiloSign App - Firma digital de documentos
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    send_file,
)
from flask_login import login_required, current_user
from ..core.utils import require_app_permission, log_audit
from .models import Document, Signature
from .forms import DocumentUploadForm, SignatureForm
import os
from datetime import datetime

# Crear blueprint para MiloSign
milosign_bp = Blueprint(
    "milosign",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/milosign",
)


@milosign_bp.route("/")
@login_required
@require_app_permission("milosign")
def dashboard():
    """Dashboard principal de MiloSign"""
    user_documents = Document.query.filter_by(owner_id=current_user.id).all()
    pending_signatures = (
        Document.query.join(Signature)
        .filter(Signature.signer_id == current_user.id, Signature.status == "pending")
        .all()
    )

    log_audit("MILOSIGN_DASHBOARD_VIEW", "milosign", current_user.id)

    return render_template(
        "milosign/dashboard.html",
        documents=user_documents,
        pending_signatures=pending_signatures,
    )


@milosign_bp.route("/upload", methods=["GET", "POST"])
@login_required
@require_app_permission("milosign")
def upload_document():
    """Subir documento para firma"""
    form = DocumentUploadForm()

    if form.validate_on_submit():
        # Procesar archivo
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join("uploads/documents", filename)
            file.save(file_path)

            # Crear registro de documento
            document = Document(
                title=form.title.data,
                description=form.description.data,
                file_path=file_path,
                original_filename=filename,
                owner_id=current_user.id,
                status="draft",
            )

            from ..core.models import db

            db.session.add(document)
            db.session.commit()

            log_audit(
                "DOCUMENT_UPLOADED",
                "milosign",
                current_user.id,
                "document",
                document.id,
            )

            flash("Documento subido correctamente.", "success")
            return redirect(url_for("milosign.document_detail", id=document.id))

    return render_template("milosign/upload.html", form=form)


@milosign_bp.route("/document/<int:id>")
@login_required
@require_app_permission("milosign")
def document_detail(id):
    """Ver detalles de un documento"""
    document = Document.query.get_or_404(id)

    # Verificar permisos
    if document.owner_id != current_user.id and not current_user.is_admin:
        # Verificar si es firmante
        signature = Signature.query.filter_by(
            document_id=id, signer_id=current_user.id
        ).first()
        if not signature:
            flash("No tienes permisos para ver este documento.", "danger")
            return redirect(url_for("milosign.dashboard"))

    signatures = Signature.query.filter_by(document_id=id).all()

    return render_template(
        "milosign/document_detail.html", document=document, signatures=signatures
    )


@milosign_bp.route("/sign/<int:document_id>", methods=["GET", "POST"])
@login_required
@require_app_permission("milosign")
def sign_document(document_id):
    """Firmar documento"""
    document = Document.query.get_or_404(document_id)
    signature = Signature.query.filter_by(
        document_id=document_id, signer_id=current_user.id
    ).first()

    if not signature:
        flash("No tienes permisos para firmar este documento.", "danger")
        return redirect(url_for("milosign.dashboard"))

    if signature.status != "pending":
        flash("Este documento ya ha sido firmado.", "info")
        return redirect(url_for("milosign.document_detail", id=document_id))

    form = SignatureForm()
    if form.validate_on_submit():
        signature.status = "signed"
        signature.signed_at = datetime.utcnow()
        signature.signature_data = form.signature_data.data
        signature.ip_address = request.remote_addr

        from ..core.models import db

        db.session.commit()

        log_audit(
            "DOCUMENT_SIGNED", "milosign", current_user.id, "document", document_id
        )

        flash("Documento firmado correctamente.", "success")
        return redirect(url_for("milosign.document_detail", id=document_id))

    return render_template(
        "milosign/sign.html", document=document, signature=signature, form=form
    )


# API endpoints
@milosign_bp.route("/api/documents")
@login_required
@require_app_permission("milosign")
def api_documents():
    """API para listar documentos del usuario"""
    documents = Document.query.filter_by(owner_id=current_user.id).all()

    return jsonify(
        [
            {
                "id": doc.id,
                "title": doc.title,
                "status": doc.status,
                "created_at": doc.created_at.isoformat(),
                "signatures_count": len(doc.signatures),
            }
            for doc in documents
        ]
    )


@milosign_bp.route("/api/document/<int:id>/status")
@login_required
@require_app_permission("milosign")
def api_document_status(id):
    """API para obtener estado de un documento"""
    document = Document.query.get_or_404(id)

    # Verificar permisos
    if document.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({"error": "Sin permisos"}), 403

    signatures = Signature.query.filter_by(document_id=id).all()

    return jsonify(
        {
            "id": document.id,
            "status": document.status,
            "signatures": [
                {
                    "signer_email": sig.signer.email,
                    "status": sig.status,
                    "signed_at": sig.signed_at.isoformat() if sig.signed_at else None,
                }
                for sig in signatures
            ],
        }
    )
