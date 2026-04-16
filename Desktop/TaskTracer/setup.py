from setuptools import setup

setup(
    name="tasktracer",
    version="1.0.0",
    py_modules=["task"], # Certifique-se que seu arquivo chama task.py
    entry_points={
        'console_scripts': [
            'tasktracer=task:main',
        ],
    },
)
