import os
import pathlib
import sys

NBS_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = NBS_DIR.parent


def init_django(project_name='cfehome', django_root='src'):
    PROJECT_ROOT = BASE_DIR / django_root
    os.chdir(PROJECT_ROOT)
    sys.path.insert(0, str(PROJECT_ROOT))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name}.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    import django

    django.setup()

if __name__ == "__main__":
    init_django()