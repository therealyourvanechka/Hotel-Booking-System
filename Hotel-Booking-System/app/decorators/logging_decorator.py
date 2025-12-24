class LoggingDecorator:
    """Декоратор для логирования вызовов методов фасада, включая ошибки."""

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __getattr__(self, name):
        attr = getattr(self._wrapped, name)

        if callable(attr):
            def logged(*args, **kwargs):
                print(f"[LOG] Вызов {name} с args={args}, kwargs={kwargs}")
                try:
                    result = attr(*args, **kwargs)
                    print(f"[LOG] Результат: {result}")
                    return result
                except Exception as e:
                    print(f"[LOG] Ошибка в {name}: {e.__class__.__name__} — {e}")
                    raise
            return logged

        return attr
