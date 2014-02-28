__author__ = 'umayloveme'


class Container:

    def __init__(self, ctrl):
        self.controller = ctrl
        self.sequence = 0
        self.shape = None
        self.prev = NullContainer()
        self.next = NullContainer()
        self.history = []

    def get_current_shape(self):
        return self.shape

    def set_current_shape(self, shape):
        self.shape = shape
        return self.controller.check_shape(self.shape)

    def retrieve_one(self):
        self.sequence = 0
        return self.controller.retrieve(history=self.history)

    def spin(self):

        if self.next.spin():
            return True

        if not self.shape:
            return False

        else:
            self.sequence += 1
            self.controller.spin_on(self)
            self.shape = self.shape.get_rotated(1, 'z')
            if self.sequence % 4 == 0:
                rotate = self.controller.order(self.sequence/4)
                if rotate:
                    self.shape = self.shape.get_rotated(*rotate)
                else:# no match result. change shape
                    self.history.append(self.shape.get_origin())
                    self.controller.put_back(self.shape)
                    self.shape = self.retrieve_one()
                    return True

            if self.controller.check_shape(self.shape):
                self.next.ready()
            return True

    def set_prev(self, container):
        self.prev = container
        # container.set_next(self)

    def get_prev(self):
        return self.prev

    def set_next(self, container):
        self.next = container

    def get_next(self):
        return self.next

    def ready(self):
        self.history = []
        new_one = self.retrieve_one()
        if new_one and self.set_current_shape(new_one):
            self.next.ready()

# class HeadContainer(Container):
#
#     def __init__(self, ctrl):
#         Container.__init__(self, ctrl)
#
#     def when_no_shape(self):
#         self.shape = self.controller.retrieve()
#         return True

class NullContainer:

    def spin(self):
        return False

    def ready(self):
        pass


class Spinner:
    def __init__(self, manipulator, shapes, max_size):
        self.manipulator = manipulator
        self.shapes = shapes
        self.length = len(shapes)
        self.containers = [Container(self) for c in range(max_size)]
        # self.containers[0] = HeadContainer(self)
        prev = None
        for c in self.containers:
            if prev:
                c.set_prev(prev)
                prev.set_next(c)
            prev = c
        self.max_size = max_size
        self.order = []

    def retrieve(self, history=[]):
        avails = [s for s in self.shapes if s not in history]
        selected = None
        if avails:
            selected = avails[-1]
            del self.shapes[self.shapes.index(selected)]
        return selected
        # return None

    def put_back(self, shape):
        self.manipulator.remove(shape)
        self.shapes.append(shape.get_origin())

    def spin_on(self, container):
        self.manipulator.remove(container.shape)

    def get_containers(self):
        return self.containers

    def ready(self):
        self.containers[0].ready()

    def set_order(self, order):
        self.order = order

    def finished(self):
        return self.length == len(self.containers[0].history)
    def spin(self):
        self.containers[0].spin()
        # map(lambda c:c.spin(), self.containers)

    def check_shape(self, shape):
        if self.manipulator.has_room(shape):
            self.manipulator.put(shape)
            return True
        return False

    def get_in_use_list(self):
        return [c.shape for c in self.containers]

    def __repr__(self):
        return 'Spinner:\navailable\t:%s\nin use\t\t:%s' % (str(self.shapes), str(self.get_in_use_list()))