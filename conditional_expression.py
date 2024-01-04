from expression import Expression

class ConditionalExpression(Expression):
    def __init__(self, condition, then_arm, else_arm):
        self.condition = condition
        self.then_arm = then_arm
        self.else_arm = else_arm

    def print(self):
        ...