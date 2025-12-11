import pytest
from pygmk2d.ecs.component import Component
from pygmk2d.ecs.entity_manager import EntityManager
from pygmk2d.ecs.system import System


# ----- Dummy Components -----

class Position(Component):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Velocity(Component):
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy


# ----- Dummy System -----

class MovementSystem(System):
    def update(self, dt: float) -> None:
        entity_ids = self._ecs.filter_entities([Position, Velocity])
        for eid in entity_ids:
            pos = self._ecs.get_component(eid, Position)
            vel = self._ecs.get_component(eid, Velocity)
            pos.x += vel.vx * dt
            pos.y += vel.vy * dt


# =====================================================
# 1. TEST ENTITY CREATION
# =====================================================

def test_create_entity():
    ecs = EntityManager()
    e1 = ecs.create_entity()
    e2 = ecs.create_entity()

    assert e1 == 0
    assert e2 == 1
    assert e2 != e1


# =====================================================
# 2. TEST ADD / REMOVE COMPONENT
# =====================================================

def test_add_component():
    ecs = EntityManager()
    eid = ecs.create_entity()

    comp = Position(10, 20)
    ecs.add_component(eid, comp)

    assert ecs.has_component(eid, Position)
    assert ecs.get_component(eid, Position).x == 10
    assert ecs.get_component(eid, Position).y == 20


def test_remove_component():
    ecs = EntityManager()
    eid = ecs.create_entity()

    ecs.add_component(eid, Position(1, 2))
    ecs.remove_component(eid, Position)

    assert not ecs.has_component(eid, Position)
    assert ecs.get_component(eid, Position) is None


def test_get_all_components():
    ecs = EntityManager()
    eid = ecs.create_entity()

    ecs.add_component(eid, Position(1, 2))
    ecs.add_component(eid, Velocity(3, 4))

    components = ecs.get_all_components(eid)

    assert "Position" in components
    assert "Velocity" in components
    assert len(components) == 2


# =====================================================
# 3. TEST ENTITY REMOVAL
# =====================================================

def test_remove_entity():
    ecs = EntityManager()
    eid = ecs.create_entity()

    ecs.add_component(eid, Position(1, 2))
    ecs.add_component(eid, Velocity(3, 4))

    ecs.remove_entity(eid)

    assert not ecs.has_component(eid, Position)
    assert not ecs.has_component(eid, Velocity)


# =====================================================
# 4. TEST QUERY BY TYPE
# =====================================================

def test_query_by_type():
    ecs = EntityManager()
    e1 = ecs.create_entity()
    e2 = ecs.create_entity()

    ecs.add_component(e1, Position(0, 0))
    ecs.add_component(e2, Position(1, 1))

    entities = ecs.query_by_type(Position)

    assert e1 in entities
    assert e2 in entities
    assert len(entities) == 2


# =====================================================
# 5. TEST FILTER ENTITIES (MULTIPLE COMPONENTS)
# =====================================================

def test_filter_entities():
    ecs = EntityManager()

    e1 = ecs.create_entity()
    e2 = ecs.create_entity()

    ecs.add_component(e1, Position(0, 0))
    ecs.add_component(e1, Velocity(1, 1))

    ecs.add_component(e2, Position(5, 5))

    result = ecs.filter_entities([Position, Velocity])

    assert e1 in result
    assert e2 not in result
    assert len(result) == 1


# =====================================================
# 6. TEST SYSTEM UPDATE
# =====================================================

def test_movement_system_update():
    ecs = EntityManager()
    system = MovementSystem(ecs)

    e = ecs.create_entity()
    ecs.add_component(e, Position(0, 0))
    ecs.add_component(e, Velocity(2, 3))

    system.update(dt=0.5)

    pos = ecs.get_component(e, Position)

    assert pos.x == 1.0   # 2 * 0.5
    assert pos.y == 1.5   # 3 * 0.5
