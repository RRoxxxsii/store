from rest_framework.exceptions import ValidationError


specialCharacters = set('?&%$#@!*')


def password_validate(password: str) -> None:
    if len(password) < 8:
        raise ValidationError("Пароль должен быть не менее 8 символов")
    if password.isalpha():
        raise ValidationError("Пароль не должен состоять только из букв")
    if password.islower():
        raise ValidationError("В пароле должен быть заглавные буквы")
    if password.isupper():
        raise ValidationError("В пароле должны быть прописные буквы")
    if not specialCharacters.intersection(password):
        raise ValidationError("В пароле должен быть как минимум один символ")


