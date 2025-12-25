# test_input_manager.py
import pytest
from unittest.mock import MagicMock
from pygmk2d.core.event_manager import EventType
from pygmk2d.input.events import RawInputType, RawInputEvent
from pygmk2d.input.manager import InputManager
from pygmk2d.input.mock_provider import MockProvider
from pygmk2d.core.mock_event_bus import MockEventBus

class TestInputManager:
    """Test suite cho InputManager"""
    
    @pytest.fixture
    def setup(self):
        """Thiết lập test environment"""
        self.mock_bus = MockEventBus()
        self.mock_provider = MockProvider()
        mock_event_manager = MagicMock()
        mock_event_manager.external = self.mock_bus
        self.input_manager = InputManager(mock_event_manager, self.mock_provider)
        return self.input_manager, self.mock_bus, self.mock_provider
    
    def test_key_down_event(self, setup):
        """Test sự kiện nhấn phím"""
        manager, bus, provider = setup
        
        # Giả lập nhấn phím A (giả sử key code 65)
        provider.add_event(RawInputEvent(
            type=RawInputType.KEY_DOWN,
            data={"key": 65}
        ))
        
        # Xử lý sự kiện
        manager.poll()
        
        # Kiểm tra
        assert manager.is_key_pressed(65) == True
        assert len(bus.events_posted) == 1
        assert bus.events_posted[0][0] == EventType.KEY_DOWN
        assert bus.events_posted[0][1]["key"] == 65
    
    def test_key_up_event(self, setup):
        """Test sự kiện thả phím"""
        manager, bus, provider = setup
        
        # Nhấn rồi thả phím
        provider.add_event(RawInputEvent(
            type=RawInputType.KEY_DOWN,
            data={"key": 65}
        ))
        provider.add_event(RawInputEvent(
            type=RawInputType.KEY_UP,
            data={"key": 65}
        ))
        
        manager.poll()
        
        # Kiểm tra
        assert manager.is_key_pressed(65) == False
        key_up_events = bus.get_events_of_type(EventType.KEY_UP)
        assert len(key_up_events) == 1
    
    def test_mouse_movement(self, setup):
        """Test di chuyển chuột"""
        manager, bus, provider = setup
        
        # Di chuyển chuột
        provider.add_event(RawInputEvent(
            type=RawInputType.MOUSE_MOVE,
            data={"pos": (100, 200)}
        ))
        
        manager.poll()
        
        # Kiểm tra
        assert manager.get_mouse_position() == (100, 200)
        mouse_events = bus.get_events_of_type(EventType.MOUSE_MOVE)
        assert len(mouse_events) == 1
        assert mouse_events[0][1]["pos"] == (100, 200)
    
    def test_mouse_button_press(self, setup):
        """Test nhấn nút chuột"""
        manager, bus, provider = setup
        
        # Nhấn nút chuột trái (giả sử button 1)
        provider.add_event(RawInputEvent(
            type=RawInputType.MOUSE_BUTTON_DOWN,
            data={"button": 1}
        ))
        
        manager.poll()
        
        # Kiểm tra
        assert manager.is_button_pressed(1) == True
        button_events = bus.get_events_of_type(EventType.MOUSE_BUTTON_DOWN)
        assert len(button_events) == 1
    
    def test_window_resize(self, setup):
        """Test thay đổi kích thước cửa sổ"""
        manager, bus, provider = setup
        
        # Thay đổi kích thước cửa sổ
        new_size = (1024, 768)
        provider.add_event(RawInputEvent(
            type=RawInputType.RESIZE,
            data={"size": new_size}
        ))
        
        manager.poll()
        
        # Kiểm tra
        assert manager.get_window_size() == new_size
        resize_events = bus.get_events_of_type(EventType.WINDOW_RESIZE)
        assert len(resize_events) == 1
    
    def test_quit_event(self, setup):
        """Test sự kiện thoát"""
        manager, bus, provider = setup
        
        # Gửi sự kiện QUIT
        provider.add_event(RawInputEvent(
            type=RawInputType.QUIT,
            data={}
        ))
        
        manager.poll()
        
        # Kiểm tra
        quit_events = bus.get_events_of_type(EventType.QUIT)
        assert len(quit_events) == 1
    
    def test_multiple_keys_pressed(self, setup):
        """Test nhiều phím được nhấn cùng lúc"""
        manager, bus, provider = setup
        
        # Nhấn nhiều phím
        keys = [65, 66, 67]  # A, B, C
        for key in keys:
            provider.add_event(RawInputEvent(
                type=RawInputType.KEY_DOWN,
                data={"key": key}
            ))
        
        manager.poll()
        
        # Kiểm tra tất cả phím đều được ghi nhận
        for key in keys:
            assert manager.is_key_pressed(key) == True
    
    def test_event_with_missing_data(self, setup):
        """Test sự kiện thiếu dữ liệu (edge case)"""
        manager, bus, provider = setup
        
        # Sự kiện KEY_DOWN nhưng không có key
        provider.add_event(RawInputEvent(
            type=RawInputType.KEY_DOWN,
            data={}  # Thiếu "key"
        ))
        
        # Không nên crash
        try:
            manager.poll()
            assert True  # Pass nếu không crash
        except Exception as e:
            pytest.fail(f"Should handle missing data gracefully: {e}")
        
        # Không có sự kiện nào được gửi
        assert len(bus.events_posted) == 0
    
    def test_consecutive_polls(self, setup):
        """Test nhiều lần poll liên tiếp"""
        manager, bus, provider = setup
        
        # Poll lần 1
        provider.add_event(RawInputEvent(
            type=RawInputType.KEY_DOWN,
            data={"key": 65}
        ))
        manager.poll()
        
        # Poll lần 2 (không có sự kiện mới)
        bus.clear()
        manager.poll()
        
        # Không có sự kiện mới
        assert len(bus.events_posted) == 0
        # Nhưng phím vẫn được giữ
        assert manager.is_key_pressed(65) == True