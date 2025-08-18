from pathlib import PosixPath
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
import re
from django.utils.translation import gettext as _

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def get_help_text(self):
        return _("La contraseña debe contener al menos %(min_length)d caracteres.") % {'min_length': self.min_length}

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("La contraseña es demasiado corta. Debe contener al menos %(min_length)d caracteres."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def __init__(self, password_list_path: PosixPath | str = ...) -> None:
        self.passwords = {"12345678", "password", "admin", "admin123"}
    def get_help_text(self):
        return _("La contraseña no debe ser demasiado común.")

    def validate(self, password, user=None):
        if password.lower() in self.passwords:
            raise ValidationError(_("La contraseña es demasiado común."), code='password_too_common')

class CombinedPasswordValidator:
    def __init__(self, forbidden_passwords=None, regex_patterns=None):
        self.forbidden_passwords = set(
            p.lower() for p in (forbidden_passwords or ["123456", "password", "admin", "qwerty"]))
        self.regex_patterns = regex_patterns or [
            r"^[A-Za-z]+\d{2}[^A-Za-z0-9]$",
            r"^[A-Za-z]+\d{4}$"
        ]

    def validate(self, password, user=None):
        pwd_lower = password.lower()

        if pwd_lower in self.forbidden_passwords:
            raise ValidationError(_("La contraseña es demasiado común."), code='password_too_common')

        for pattern in self.regex_patterns:
            if re.match(pattern, password):
                raise ValidationError(
                    _("La contraseña sigue un patrón predecible. Usa algo más aleatorio."),
                    code='password_pattern_common'
                )

        if not re.search(r"[A-Z]", password):
            raise ValidationError(_("La contraseña debe contener al menos una letra mayúscula."), code='password_no_upper')

        if not re.search(r"[a-z]", password):
            raise ValidationError(_("La contraseña debe contener al menos una letra minúscula."), code='password_no_lower')

        if not re.search(r"\d", password):
            raise ValidationError(_("La contraseña debe contener al menos un número."), code='password_no_digit')

        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError(_("La contraseña debe contener al menos un símbolo."), code='password_no_symbol')

    def get_help_text(self):
        return _(
            "La contraseña debe tener caracteres, incluir mayúsculas, "
            "minúsculas, números y símbolos, y no seguir patrones comunes."
        )

class CustomNumericPasswordValidator(NumericPasswordValidator):
    def get_help_text(self):
        return _("La contraseña no puede contener solo números.")

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(_("La contraseña no puede ser solo números."), code='password_entirely_numeric')
