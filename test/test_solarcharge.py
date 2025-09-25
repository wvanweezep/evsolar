import pytest

from freezegun import freeze_time

from commons.debug import Debug
from mock.nrgkick import MockNRGKick
from services.solarcharge import SolarCharge


@pytest.fixture
def setup():
    Debug.VERBOSITY = 0
    with freeze_time("2025-01-01 10:00:00"):
        mock_nrg: MockNRGKick = MockNRGKick("CONNECTED", 3, 12)
        sc: SolarCharge = SolarCharge(mock_nrg)
    return sc, mock_nrg


def test_start(setup):
    sc, nrg = setup

    with freeze_time("2025-01-01 10:00:59"):
        sc.update(-7, nrg.current)
        assert nrg.phase_count == 3

    with freeze_time("2025-01-01 10:01:00"):
        sc.update(-7, nrg.current)
        assert nrg.phase_count == 1


def test_stop(setup):
    sc, nrg = setup

    with freeze_time("2025-01-01 10:01:00"):
        sc.update(-7, nrg.current)
        assert nrg.status == "CHARGING"
        sc.update(nrg.current, nrg.current)

    with freeze_time("2025-01-01 10:01:59"):
        sc.update(nrg.current, nrg.current)
        assert nrg.status == "CHARGING"

    with freeze_time("2025-01-01 10:02:00"):
        sc.update(nrg.current, nrg.current)
        assert nrg.status == "CONNECTED"


def test_regulated_current(setup):
    sc, nrg = setup

    with freeze_time("2025-01-01 10:01:00"):
        sc.update(-7, nrg.current)
        assert nrg.status == "CHARGING"
        assert nrg.current == 12

    with freeze_time("2025-01-01 10:01:10"):
        sc.update(5, nrg.current)
        sc.update(5, nrg.current)
        assert nrg.current == 7

    with freeze_time("2025-01-01 10:01:20"):
        sc.update(-2.2, nrg.current)
        sc.update(-2.2, nrg.current)
        assert nrg.current == 9.2






