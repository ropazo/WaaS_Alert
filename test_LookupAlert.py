from unittest import TestCase
from LookupAlert import lookup_alert
import ScheduleLookup

response_with_dump = {
    "OperationId": "1ac3c436-c709-478f-b5b4-f3bc84c45f03",
    "Status": "ERROR",
    "Message": "Por favor, inténtalo más tarde",
    "FailureReason": "TASK_DUMPED",
}


class TestLookupAlert(TestCase):

    def test_basic_call(self):
        r_json = lookup_alert(office="Valencia/València", country="Chile")
        print(f'Respuesta recibida\n\tStatus = {r_json["Status"]}\n\tMensaje = {r_json["Message"]}')

    def test_schedule_lookup(self):
        ScheduleLookup.schedule_lookup()
