import json
from typing import List, Dict, Any


class DomainElement:
    """领域模型元素的基类"""

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.name}"


class DomainScenario(DomainElement):
    """领域场景 (Domain Scenario)"""

    def __init__(self, name: str, context: 'Context', state_sets: List['StateSet']):
        super().__init__(name)
        self.context = context  # 上下文对象
        self.state_sets = state_sets  # 状态集列表


class Context(DomainElement):
    """上下文 (Context)"""

    def __init__(self, name: str, description: str = ""):
        super().__init__(name)
        self.description = description


class StateSet(DomainElement):
    """状态集 (State Set)"""

    def __init__(self, name: str, states: List['State']):
        super().__init__(name)
        self.states = states  # 状态对象列表


class State(DomainElement):
    """状态 (State)"""

    def __init__(self, name: str, attributes: List['Attribute'] = None):
        super().__init__(name)
        self.attributes = attributes or []  # 属性对象列表


class Entity(DomainElement):
    """实体 (Entity)"""

    def __init__(self, name: str, attributes: List['Attribute'] = None):
        super().__init__(name)
        self.attributes = attributes or []  # 属性对象列表


class Event(DomainElement):
    """事件 (Event)"""

    def __init__(self, name: str, actions: List['Action'] = None, params: List['Param'] = None):
        super().__init__(name)
        self.actions = actions or []  # 动作对象列表
        self.params = params or []  # 参数对象列表


class Action(DomainElement):
    """动作 (Action)"""

    def __init__(self, name: str, params: List['Param'] = None):
        super().__init__(name)
        self.params = params or []  # 参数对象列表


class Attribute(DomainElement):
    """属性 (Attribute)"""

    def __init__(self, name: str, data_type: str):
        super().__init__(name)
        self.data_type = data_type  # 数据类型


class Param(DomainElement):
    """参数 (Param)"""

    def __init__(self, name: str, data_type: str):
        super().__init__(name)
        self.data_type = data_type  # 数据类型


class DomainModelAssembler:
    """领域模型组装器"""

    def __init__(self):
        self.domain_scenarios = []
        self.entities = []
        self.events = []

    def load_from_json(self, file_path: str) -> None:
        """
        从JSON文件加载领域要素并组装模型
        :param file_path: JSON文件路径
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 创建上下文
        context = Context(data['context']['name'], data['context'].get('description', ''))

        # 创建状态集和状态
        state_sets = []
        for state_set_data in data['state_sets']:
            states = []
            for state_data in state_set_data['states']:
                attributes = [
                    Attribute(attr['name'], attr['type'])
                    for attr in state_data.get('attributes', [])
                ]
                states.append(State(state_data['name'], attributes))
            state_sets.append(StateSet(state_set_data['name'], states))

        # 创建领域场景
        scenario = DomainScenario(data['scenario']['name'], context, state_sets)
        self.domain_scenarios.append(scenario)

        # 创建实体
        for entity_data in data['entities']:
            attributes = [
                Attribute(attr['name'], attr['type'])
                for attr in entity_data.get('attributes', [])
            ]
            self.entities.append(Entity(entity_data['name'], attributes))

        # 创建事件
        for event_data in data['events']:
            params = [
                Param(param['name'], param['type'])
                for param in event_data.get('params', [])
            ]

            actions = []
            for action_data in event_data.get('actions', []):
                action_params = [
                    Param(param['name'], param['type'])
                    for param in action_data.get('params', [])
                ]
                actions.append(Action(action_data['name'], action_params))

            self.events.append(Event(event_data['name'], actions, params))

    def display_model(self) -> None:
        """显示完整的领域模型结构"""
        print("\n" + "=" * 50)
        print("领域模型结构")
        print("=" * 50)

        # 打印领域场景
        for i, scenario in enumerate(self.domain_scenarios, 1):
            print(f"\n领域场景 #{i}: {scenario.name}")
            print(f"  上下文: {scenario.context.name}")
            if scenario.context.description:
                print(f"    描述: {scenario.context.description}")

            for j, state_set in enumerate(scenario.state_sets, 1):
                print(f"  状态集 #{j}: {state_set.name}")

                for k, state in enumerate(state_set.states, 1):
                    print(f"    状态 #{k}: {state.name}")
                    for attr in state.attributes:
                        print(f"      - 属性: {attr.name} ({attr.data_type})")

        # 打印实体
        print("\n实体:")
        for entity in self.entities:
            print(f"  {entity.name}")
            for attr in entity.attributes:
                print(f"    - 属性: {attr.name} ({attr.data_type})")

        # 打印事件
        print("\n事件:")
        for event in self.events:
            print(f"  {event.name}")
            for param in event.params:
                print(f"    - 参数: {param.name} ({param.data_type})")

            for action in event.actions:
                print(f"    - 动作: {action.name}")
                for param in action.params:
                    print(f"        > 参数: {param.name} ({param.data_type})")


# 示例JSON文件路径
JSON_FILE_PATH = "model_element.json"

# 使用示例
if __name__ == "__main__":
    assembler = DomainModelAssembler()

    # 从JSON文件加载领域要素
    assembler.load_from_json(JSON_FILE_PATH)

    # 显示完整模型
    assembler.display_model()