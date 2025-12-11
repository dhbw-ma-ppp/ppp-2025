import time
from matplotlib import pyplot as plt
from matplotlib.backend_bases import Event, KeyEvent
from matplotlib.figure import Figure


class UserController:
    def __init__(self, fig: Figure):
        self.fig = fig
        self._cid = fig.canvas.mpl_connect("key_press_event", self.on_key)
        self._key_input_queue: list[KeyEvent] = []

    def on_key(self, event: Event):
        if isinstance(event, KeyEvent):
            self._key_input_queue.append(event)

    def dispose(self):
        if self._cid is not None:
            self.fig.canvas.mpl_disconnect(self._cid)
            self._cid = None
        self._key_input_queue.clear()

    def get_next_key_input(
        self,
        case_sensitive=True,
        accept: list | None = None,
        replace_by_key: dict[object, list[str]] | None = None,
        timeout: float | None = None,
    ):
        self._key_input_queue.clear()
        start_time = time.time()
        elapsed = 0

        flattened_accept_keys = []
        if isinstance(accept, list):
            for a in accept:
                if isinstance(a, (list, tuple)):
                    flattened_accept_keys.extend(a)
                else:
                    flattened_accept_keys.append(a)

        while elapsed < (timeout if timeout is not None else float("inf")):
            if self._key_input_queue:
                event = self._key_input_queue.pop(0)
                key = event.key
                if not isinstance(key, str):
                    continue

                if not case_sensitive:
                    key = key.lower()

                if flattened_accept_keys and key not in flattened_accept_keys:
                    continue

                if isinstance(replace_by_key, dict):
                    for resulting_key, before_key in replace_by_key.items():
                        if key in before_key:
                            return resulting_key

                return key

            plt.pause(0.05)
            elapsed = time.time() - start_time

        return None
