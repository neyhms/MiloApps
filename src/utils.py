"""
InfoMilo - Utilidades de Autenticación
Funciones auxiliares para seguridad y análisis de sesiones
"""

from datetime import datetime
from flask import request
from user_agents import parse
import re
import hashlib

def get_client_info(request_obj):
    """Extrae información del cliente desde la petición"""
    ua_string = request_obj.user_agent.string
    ua = parse(ua_string)
    
    return {
        'ip_address': request_obj.remote_addr,
        'user_agent': ua_string,
        'browser': f"{ua.browser.family} {ua.browser.version_string}",
        'os': f"{ua.os.family} {ua.os.version_string}",
        'device': ua.device.family,
        'is_mobile': ua.is_mobile,
        'is_tablet': ua.is_tablet,
        'is_pc': ua.is_pc,
        'is_bot': ua.is_bot,
        'timestamp': datetime.utcnow()
    }

def is_suspicious_login(user, request_obj):
    """Detecta si un login puede ser sospechoso"""
    current_ip = request_obj.remote_addr
    
    # Si es el primer login, no es sospechoso
    if not user.last_login_ip:
        return False
    
    # Si la IP es diferente a la última conocida
    if user.last_login_ip != current_ip:
        return True
    
    # Si han pasado más de 30 días desde el último login
    if user.last_login:
        days_since_last = (datetime.utcnow() - user.last_login).days
        if days_since_last > 30:
            return True
    
    return False

def generate_session_id():
    """Genera un ID de sesión único"""
    import secrets
    return secrets.token_urlsafe(32)

def hash_ip_address(ip_address):
    """Hash una dirección IP para anonimización"""
    return hashlib.sha256(ip_address.encode()).hexdigest()[:16]

def is_valid_password(password):
    """Valida que una contraseña cumpla los requisitos de seguridad"""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    # Opcional: caracteres especiales
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #     return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, "Contraseña válida"

def generate_secure_password(length=12):
    """Genera una contraseña segura aleatoria"""
    import secrets
    import string
    
    # Asegurar que tenga al menos uno de cada tipo
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*")
    ]
    
    # Completar con caracteres aleatorios
    for _ in range(length - 4):
        password.append(secrets.choice(string.ascii_letters + string.digits))
    
    # Mezclar la lista
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def calculate_password_strength(password):
    """Calcula la fortaleza de una contraseña (0-100)"""
    score = 0
    
    # Longitud
    if len(password) >= 8:
        score += 20
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10
    
    # Tipos de caracteres
    if re.search(r'[a-z]', password):
        score += 10
    if re.search(r'[A-Z]', password):
        score += 10
    if re.search(r'\d', password):
        score += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 15
    
    # Variedad
    unique_chars = len(set(password))
    if unique_chars >= len(password) * 0.7:
        score += 15
    
    return min(score, 100)

def get_password_strength_text(score):
    """Convierte el puntaje de fortaleza a texto"""
    if score < 30:
        return "Muy débil", "danger"
    elif score < 50:
        return "Débil", "warning"
    elif score < 70:
        return "Regular", "info"
    elif score < 90:
        return "Fuerte", "success"
    else:
        return "Muy fuerte", "success"

def sanitize_input(text, max_length=None):
    """Sanitiza entrada de usuario"""
    if not text:
        return ""
    
    # Eliminar espacios en blanco al inicio y final
    text = text.strip()
    
    # Limitar longitud si se especifica
    if max_length:
        text = text[:max_length]
    
    return text

def is_safe_url(target):
    """Verifica si una URL es segura para redirección"""
    from urllib.parse import urlparse, urljoin
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def format_datetime_user_friendly(dt):
    """Formatea fecha/hora de manera amigable"""
    if not dt:
        return "Nunca"
    
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 365:
        years = diff.days // 365
        return f"Hace {years} año{'s' if years > 1 else ''}"
    elif diff.days > 30:
        months = diff.days // 30
        return f"Hace {months} mes{'es' if months > 1 else ''}"
    elif diff.days > 0:
        return f"Hace {diff.days} día{'s' if diff.days > 1 else ''}"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"Hace {hours} hora{'s' if hours > 1 else ''}"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"Hace {minutes} minuto{'s' if minutes > 1 else ''}"
    else:
        return "Hace unos segundos"

def get_gravatar_url(email, size=80, default='identicon'):
    """Genera URL de Gravatar para un email"""
    import hashlib
    
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}"

def mask_email(email):
    """Enmascara un email para mostrar parcialmente"""
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    
    if len(local) <= 2:
        masked_local = local[0] + '*'
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"

def mask_phone(phone):
    """Enmascara un número de teléfono"""
    if not phone or len(phone) < 4:
        return phone
    
    return phone[:2] + '*' * (len(phone) - 4) + phone[-2:]

def validate_phone_number(phone):
    """Valida formato de número de teléfono"""
    if not phone:
        return True  # Opcional
    
    # Formato básico: números, espacios, +, -, (, )
    pattern = r'^[\+]?[\d\s\-\(\)]{7,20}$'
    return bool(re.match(pattern, phone))

def extract_domain_from_email(email):
    """Extrae el dominio de un email"""
    if '@' in email:
        return email.split('@')[1].lower()
    return ""

def is_business_email(email):
    """Detecta si es un email corporativo (no gratuito)"""
    domain = extract_domain_from_email(email)
    
    free_providers = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'aol.com', 'icloud.com', 'mail.com', 'gmx.com'
    ]
    
    return domain not in free_providers

def generate_username_suggestions(first_name, last_name, existing_usernames=None):
    """Genera sugerencias de nombres de usuario"""
    if existing_usernames is None:
        existing_usernames = set()
    
    suggestions = []
    first = first_name.lower().strip()
    last = last_name.lower().strip()
    
    # Combinaciones básicas
    combinations = [
        f"{first}.{last}",
        f"{first}{last}",
        f"{first}_{last}",
        f"{first[0]}{last}",
        f"{first}{last[0]}",
        f"{last}.{first}",
        f"{last}_{first}"
    ]
    
    # Agregar números si ya existen
    for combo in combinations[:3]:  # Solo las primeras 3
        if combo not in existing_usernames:
            suggestions.append(combo)
        else:
            for i in range(1, 100):
                suggestion = f"{combo}{i}"
                if suggestion not in existing_usernames:
                    suggestions.append(suggestion)
                    break
    
    return suggestions[:5]  # Máximo 5 sugerencias

def log_security_event(
    event_type,
    description,
    user_id=None,
    ip_address=None,
    additional_data=None,
):
    """Log eventos de seguridad críticos"""
    from .models import log_audit_event
    
    log_audit_event(
        user_id=user_id,
        event_type=f"SECURITY_{event_type}",
        description=description,
        request=None,  # Se puede pasar request si está disponible
        additional_data=additional_data
    )
    
    # También log en archivo si es crítico
    import logging
    security_logger = logging.getLogger('security')
    security_logger.warning(
        f"{event_type}: {description} - User: {user_id} - IP: {ip_address}"
    )


def check_rate_limit(key, limit=5, window=300):
    """Implementación básica de rate limiting"""
    # Esta es una implementación simple en memoria
    # Para producción usar Redis o similar
    
    import time
    
    if not hasattr(check_rate_limit, 'cache'):
        check_rate_limit.cache = {}
    
    now = time.time()
    
    # Limpiar entradas antiguas
    check_rate_limit.cache = {
        k: v for k, v in check_rate_limit.cache.items()
        if now - v['first_attempt'] < window
    }
    
    if key not in check_rate_limit.cache:
        check_rate_limit.cache[key] = {
            'count': 1,
            'first_attempt': now
        }
        return True
    
    entry = check_rate_limit.cache[key]
    
    if entry['count'] >= limit:
        return False
    
    entry['count'] += 1
    return True
