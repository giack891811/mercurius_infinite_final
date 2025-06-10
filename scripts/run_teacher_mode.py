"""Avvia la Teacher Mode isolata."""
from modules.teacher_mode import TeacherMode


def start():
    teacher = TeacherMode()
    teacher.toggle(True)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        teacher.toggle(False)


if __name__ == "__main__":
    start()
