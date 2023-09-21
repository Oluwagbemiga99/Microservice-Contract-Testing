from core.TestRunner import Runner
from models import Test


class MasterRunner:

    running = False
    current_test = None
    class __Master:
        def __init__(self, arg):
            self.val = arg

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, arg):
        if not MasterRunner.instance:
            MasterRunner.instance = MasterRunner.__Master(arg)
        else:
            MasterRunner.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)


    @staticmethod
    def runTest(test: Test):
        def finished_callback():
            MasterRunner.running = False
            MasterRunner.current_test = None
        runner = Runner(test, finished_callback)
        MasterRunner.running = True
        MasterRunner.current_test = test
        runner.start()

    
