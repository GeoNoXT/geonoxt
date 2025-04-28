from django.core.management.base import BaseCommand
from celery import current_app
from geonode.celery_app import app

class Command(BaseCommand):
    help = "Ejecuta tareas de Celery de forma síncrona, sin asincronía"

    def add_arguments(self, parser):
        parser.add_argument('task_name', type=str, help='El nombre de la tarea de Celery')
        parser.add_argument('task_args', nargs='*', help='Argumentos de la tarea', default=[])

    def handle(self, *args, **options):
        task_name = options['task_name']
        task_args = options['task_args']

        try:
            # Importar la tarea de Celery usando el nombre proporcionado
            task = app.tasks[task_name]
        except KeyError:
            self.stderr.write(f"Tarea '{task_name}' no encontrada.")
            return

        # Convertir los argumentos a los tipos correctos, si es necesario
        task_args = [self._parse_argument(arg) for arg in task_args]

        try:
            # Ejecutar la tarea de forma síncrona (sin asincronía)
            result = task.run(*task_args)

            # Mostrar el resultado de la ejecución
            self.stdout.write(f"Tarea ejecutada exitosamente, resultado: {result}")
        except Exception as e:
            self.stderr.write(f"Error al ejecutar la tarea: {e}")

    def _parse_argument(self, arg):
        """Convierte un argumento de texto a su tipo correspondiente."""
        if arg.isdigit():
            return int(arg)
        try:
            # Intenta convertir a float si es posible
            return float(arg)
        except ValueError:
            # Si no es número, devolver como cadena
            return arg