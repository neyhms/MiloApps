import os
import sys
import unittest

# Ensure 'src' is on the Python path when running tests from repo root
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from flask import Flask  # noqa: E402

from models import (  # noqa: E402
    db,
    User,
    Role,
    Application,
    Functionality,
    RoleAppAccess,
    RoleFunctionality,
)


class PermissionModelTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            SECRET_KEY="test",
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SQLALCHEMY_EXPIRE_ON_COMMIT=False,
            WTF_CSRF_ENABLED=False,
            TESTING=True,
        )
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            # seed basic roles and app
            role_admin = Role(name="admin", display_name="Administrador")
            role_all = Role(
                name="ALLMILO",
                display_name="Acceso Global",
                is_allmilo=True,
            )
            role_sign = Role(
                name="sign_manager",
                display_name="Gestor MiloSign",
            )
            db.session.add_all([role_admin, role_all, role_sign])

            app_milosign = Application(key="milosign", name="MiloSign")
            db.session.add(app_milosign)
            db.session.flush()
            func_create = Functionality(
                application_id=app_milosign.id,
                key="create",
                name="Crear",
            )
            func_view = Functionality(
                application_id=app_milosign.id,
                key="view",
                name="Ver",
            )
            db.session.add_all([func_create, func_view])
            db.session.commit()

            # store IDs to avoid detached instances between app contexts
            self.role_admin_id = role_admin.id
            self.role_all_id = role_all.id
            self.role_sign_id = role_sign.id
            self.app_milosign_id = app_milosign.id
            self.func_create_id = func_create.id
            self.func_view_id = func_view.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def make_user(
        self, email: str, primary_role_id: int | None = None
    ) -> User:
        # Assumes caller already within app_context
        u = User(
            email=email,
            username=email.split("@")[0],
            first_name="Test",
            last_name="User",
            role_id=primary_role_id if primary_role_id else None,
            is_active=True,
            is_verified=True,
        )
        u.set_password("secret123A")
        db.session.add(u)
        db.session.commit()
        return u

    def test_allmilo_grants_full_access(self):
        with self.app.app_context():
            u = self.make_user(
                "all@milo.com", primary_role_id=self.role_all_id
            )
            self.assertTrue(u.has_app_access("milosign"))
            self.assertTrue(u.has_functionality("milosign", "create"))

    def test_full_app_access_via_role(self):
        with self.app.app_context():
            u = self.make_user("fa@milo.com")
            # re-query role and app within current session
            role_sign = Role.query.get(self.role_sign_id)
            u.roles.append(role_sign)
            db.session.add(
                RoleAppAccess(
                    role_id=self.role_sign_id,
                    app_id=self.app_milosign_id,
                    full_access=True,
                )
            )
            db.session.commit()
            self.assertTrue(u.has_app_access("milosign"))
            self.assertTrue(u.has_functionality("milosign", "view"))

    def test_granular_functionality(self):
        with self.app.app_context():
            u = self.make_user("gran@milo.com")
            role_sign = Role.query.get(self.role_sign_id)
            u.roles.append(role_sign)
            db.session.add(
                RoleFunctionality(
                    role_id=self.role_sign_id,
                    functionality_id=self.func_create_id,
                )
            )
            db.session.commit()
            # Acceso a la app por tener alguna funcionalidad
            self.assertTrue(u.has_app_access("milosign"))
            # Tiene permiso a 'create' pero no necesariamente a otra
            # si no hay full_access
            self.assertTrue(u.has_functionality("milosign", "create"))
            self.assertFalse(u.has_functionality("milosign", "view"))


if __name__ == "__main__":
    unittest.main()
