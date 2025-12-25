import pytest
import time

from pygmk2d.ecs.entity_manager import EntityManager
from pygmk2d.ecs.component import Component


# -------------------------------------------------
# Dummy Components
# -------------------------------------------------
class Position(Component):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Health(Component):
    def __init__(self, value=100):
        self.value = value


# -------------------------------------------------
# Fixture
# -------------------------------------------------
@pytest.fixture
def ecs():
    return EntityManager()


# -------------------------------------------------
# AVAILABILITY TESTING
# -------------------------------------------------

def test_ecs_availability_basic_access(ecs):
    """
    Kiểm thử khả năng truy cập ECS:
    - Tạo entity
    - Thêm component
    - Truy cập component liên tục
    """
    entity = ecs.create_entity()
    ecs.add_component(entity, Position(10, 20))

    for _ in range(1000):
        assert ecs.has_component(entity, Position)
        assert ecs.get_component(entity, Position) is not None


# -------------------------------------------------
# LOAD TESTING
# -------------------------------------------------

def test_ecs_load_many_entities(ecs):
    """
    Kiểm thử ECS với số lượng lớn entity
    """
    entity_count = 10_000

    start = time.time()
    entities = [ecs.create_entity() for _ in range(entity_count)]

    for e in entities:
        ecs.add_component(e, Position())
        ecs.add_component(e, Health())

    duration = time.time() - start

    assert len(entities) == entity_count
    print(f"[LOAD] {entity_count} entities processed in {duration:.2f}s")


# -------------------------------------------------
# STRESS TESTING
# -------------------------------------------------

def test_ecs_stress_extreme_load(ecs):
    """
    Kiểm thử ECS với tải cực lớn
    """
    entity_count = 50_000

    entities = [ecs.create_entity() for _ in range(entity_count)]
    for e in entities:
        ecs.add_component(e, Position())

    # Truy cập hàng loạt
    for _ in range(10):
        result = ecs.query_by_type(Position)
        assert len(result) == entity_count


# -------------------------------------------------
# HIGH-FREQUENCY ACCESS TESTING
# -------------------------------------------------

def test_ecs_high_frequency_access(ecs):
    """
    Kiểm thử truy cập ECS với tần suất cao
    """
    entity = ecs.create_entity()
    ecs.add_component(entity, Position())

    for _ in range(100_000):
        ecs.get_component(entity, Position)

