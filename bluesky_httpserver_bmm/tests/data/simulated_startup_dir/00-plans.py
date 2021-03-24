# Contain plan headers for testing of queue execution for BMM beamline
# Plans: mv, xafs, change_edge, shb_close_plan, set_slot

from ophyd.sim import hw

from bluesky.plans import count, scan
from bluesky.plan_stubs import mv  # noqa: F401

from bluesky_queueserver.manager.profile_tools import set_user_ns

det1, det2, motor = hw().det1, hw().det2, hw().motor

# Those are devices used with 'mv' plans
xafs_x = motor
xafs_y = motor
slits3_hsize = motor
xafs_det = motor


@set_user_ns
def xafs(inifile=None, *, user_ns, **kwargs):
    yield from count([det1, det2], num=5, delay=1)


@set_user_ns
def change_edge(
    el, focus=False, edge="K", energy=None, slits=True, target=300.0, xrd=False, bender=True, *, user_ns
):
    yield from scan([det1, det2], motor, -1, 1, 10)


def shb_close_plan():
    yield from count([det1, det2])


def set_slot(self, n):
    yield from count([det1])
