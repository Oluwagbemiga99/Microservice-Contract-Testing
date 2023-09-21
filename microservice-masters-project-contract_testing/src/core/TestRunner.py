from typing import Callable
from unittest import TestSuite
from config import Config
from models.Test import Result, Test
from core.TestCase import ContractTest
import HtmlTestRunner
from threading import Thread


class Runner(Thread):

    
    def __init__(self, test: Test, on_finish_callback: Callable) -> None:
        super(Runner, self).__init__()
        self.test = test
        self.on_finish_callback = on_finish_callback

    def run(self):
        suite = TestSuite()
        for contract in self.test.contracts:
            if(contract.skip):
                continue
            s = None
            for schema in self.test.schemas:
                if contract.schemaId == schema.id:
                    s = schema
            suite.addTest(
                ContractTest(service=self.test.service, contract=contract, schema=s)
            )
        out_parent_dir =  "./" + Config.results_dir + "/" + self.test.id
        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_name=Config.report_file_name,
            output=out_parent_dir,
            report_title=self.test.name + "_" + self.test.id,
            add_timestamp=False,
        )
        runnerResults = runner.run(suite)
        results = Result(
            total=runnerResults.testsRun,
            passed=runnerResults.testsRun - len(runnerResults.failures),
            failed=len(runnerResults.failures),
            reportPath=out_parent_dir + "/" + Config.report_file_name + ".html",
            wasSuccessful=runnerResults.wasSuccessful(),
            duration=runner.time_taken.total_seconds(),
        )
        self.test.results = results
        try:
            with open(out_parent_dir + "/results.json", mode="w") as file:
                file.writelines(self.test.model_dump_json())
        except Exception as e:
            pass
        self.on_finish_callback()

