from typing import Optional
import unittest
import unittest.result
from jsonschema import validate
from config import Config
from models.Contract import Contract
from models.Service import Service
from models.Schema import Schema
import requests
import time

class ContractTest(unittest.TestCase):
    def __init__(
        self, service: Service, contract: Contract, schema: Optional[Schema]
    ) -> None:
        super(ContractTest, self).__init__()
        self.contract = contract
        self.service = service
        self.schema = schema

    def runTest(self):
        self._testMethodName = (
            self.contract.description if self.contract.description else "Unnamed test"
        )
        headers = {}
        if self.contract.authorized:
            headers["X-API-KEY"] = self.service.api_key
        try:
            response = requests.request(
                self.contract.method,
                headers=headers,
                url=self.service.url + self.contract.route,
                json=self.contract.data,
                timeout=self.contract.max_time_taken_sec or 2,
                verify=False,
            )
            print(response.text)
            self.assertEqual(
                response.status_code,
                self.contract.expected_status_code,
                msg="Different status code than {} returned".format(
                    self.contract.expected_status_code
                ),
            )
            if self.schema:
                try:
                    validate(instance=response.json(), schema=self.schema.jsonSchema)
                except Exception as e:
                    self.fail(str(e))
        except requests.exceptions.Timeout:
            self.fail(
                "Request failed: timeout exceeded {} second(s)".format(
                    self.contract.max_time_taken_sec
                )
            )
        except requests.exceptions.TooManyRedirects:
            self.fail("Request failed:Too many redirects")
        except requests.exceptions.RequestException as e:
            self.fail("Request failed:" + str(e))
        except Exception as e:
            self.fail(str(e))
        finally:
            time.sleep(Config.time_between_test_sec)
