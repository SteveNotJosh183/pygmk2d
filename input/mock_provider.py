# test_providers.py
from typing import Iterable, List
from .events import RawInputEvent, RawInputType
from .provider import InputProvider


class MockProvider(InputProvider):
    """Provider giả lập để kiểm thử"""
    def __init__(self):
        self.events_queue: List[RawInputEvent] = []
        self.poll_count = 0
    
    def add_event(self, event: RawInputEvent):
        """Thêm sự kiện vào hàng đợi"""
        self.events_queue.append(event)
    
    def clear_events(self):
        """Xóa tất cả sự kiện"""
        self.events_queue.clear()
    
    def poll(self) -> Iterable[RawInputEvent]:
        """Trả về các sự kiện trong hàng đợi"""
        self.poll_count += 1
        events = list(self.events_queue)
        self.events_queue.clear()
        return events


class KeyboardOnlyProvider(MockProvider):
    """Provider chỉ giả lập bàn phím"""
    def simulate_key_press(self, key: int):
        """Giả lập nhấn và thả phím"""
        self.add_event(RawInputEvent(
            type=RawInputType.KEY_DOWN,
            data={"key": key}
        ))
    
    def simulate_key_release(self, key: int):
        self.add_event(RawInputEvent(
            type=RawInputType.KEY_UP,
            data={"key": key}
        ))


class MouseOnlyProvider(MockProvider):
    """Provider chỉ giả lập chuột"""
    def simulate_mouse_move(self, x: int, y: int):
        self.add_event(RawInputEvent(
            type=RawInputType.MOUSE_MOVE,
            data={"pos": (x, y)}
        ))
    
    def simulate_mouse_click(self, button: int):
        """Giả lập nhấn và thả nút chuột"""
        self.add_event(RawInputEvent(
            type=RawInputType.MOUSE_BUTTON_DOWN,
            data={"button": button}
        ))
        self.add_event(RawInputEvent(
            type=RawInputType.MOUSE_BUTTON_UP,
            data={"button": button}
        ))