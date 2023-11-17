from threading import Thread

from src.gui.gui import run_app


def main():
    window_thread = Thread(target=run_app,
                           daemon=True)

    window_thread.start()
    window_thread.join()


if __name__ == '__main__':
    main()
