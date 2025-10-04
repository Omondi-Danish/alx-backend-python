from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'messaging'

    def ready(self):
        # import the signals module to ensure signal handlers are connected
        import messaging.signals  # noqa
