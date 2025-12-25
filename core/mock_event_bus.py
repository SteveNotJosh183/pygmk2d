# test_mocks.py
from typing import Dict, List
from .event_manager import EventType


class MockEventBus:
    """Mock cho EventBus để kiểm tra sự kiện được gửi"""
    def __init__(self):
        self.events_posted: List[tuple] = []
        self.handlers: Dict[EventType, List[callable]] = {}
    
    def post(self, event_type: EventType, data: dict):
        """Ghi lại sự kiện được gửi"""
        self.events_posted.append((event_type, data))
        # Gọi handlers nếu có
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                handler(data)
    
    def register(self, event_type: EventType, handler: callable):
        """Đăng ký handler cho sự kiện"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def clear(self):
        """Xóa tất cả sự kiện đã ghi"""
        self.events_posted.clear()
    
    def get_events_of_type(self, event_type: EventType):
        """Lấy tất cả sự kiện của một loại"""
        return [e for e in self.events_posted if e[0] == event_type]