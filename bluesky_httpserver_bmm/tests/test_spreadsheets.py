import os
import pytest
import pkg_resources

from bluesky_httpserver_bmm import spreadsheet_to_plan_list


def _get_sample_data_dir():
    """
    Returns the path to the default profile collection that is distributed with the package.
    The function does not guarantee that the directory exists.
    """
    pc_path = pkg_resources.resource_filename("bluesky_httpserver_bmm", "tests/data/")
    return pc_path


# fmt: off
@pytest.mark.parametrize("ss_file_name, plan_list", [
    ("sample_ss_wheel_xafs_1.xlsx",
     [{'name': 'slot', 'args': [13], 'kwargs': {}},
      {'name': 'mv', 'args': ['xafs_det', 28], 'kwargs': {}},
      {'name': 'xafs',
       'args': [],
       'kwargs': {'filename': 'DyTFO_Ti',
                  'nscans': 8,
                  'start': 'next',
                  'mode': 'both',
                  'element': 'Ti',
                  'edge': 'K',
                  'sample': 'Dy2Ti0.75Fe0.25O5',
                  'prep': 'Powder in PEG',
                  'comment': '1500(48)',
                  'bounds': '-200 -30 -10 30 12k',
                  'steps': '10 2 0.2 0.05k',
                  'times': '1 1 1 1',
                  'snapshots': True,
                  'htmlpage': True,
                  'usbstick': True,
                  'bothways': False,
                  'channelcut': False,
                  'ththth': False,
                  'url': '...',
                  'doi': '...',
                  'cif': '...',
                  'experimenters': 'User One / User Two / User Three'}},
      {'name': 'slot', 'args': [13], 'kwargs': {}},
      {'name': 'mv', 'args': ['xafs_det', 80], 'kwargs': {}},
      {'name': 'change_edge',
       'args': ['Fe'],
       'kwargs': {'edge': 'K', 'focus': False}},
      {'name': 'xafs',
       'args': [],
       'kwargs': {'filename': 'DyTFO_Fe',
                  'nscans': 8,
                  'start': 'next',
                  'mode': 'both',
                  'element': 'Fe',
                  'edge': 'K',
                  'sample': 'Dy2Ti0.75Fe0.25O5',
                  'prep': 'Powder in PEG',
                  'comment': '1500(48)',
                  'bounds': '-200 -30 -10 30 12k',
                  'steps': '10 2 0.2 0.05k',
                  'times': '1 1 1 1',
                  'snapshots': True,
                  'htmlpage': True,
                  'usbstick': True,
                  'bothways': False,
                  'channelcut': False,
                  'ththth': False,
                  'url': '...',
                  'doi': '...',
                  'cif': '...',
                  'experimenters': 'User One / User Two / User Three'}},
      {'name': 'shb_close_plan', 'args': [], 'kwargs': {}}]),
])
# fmt: on
def test_spreadsheets_1(ss_file_name, plan_list):
    dir = _get_sample_data_dir()
    ss_path = os.path.join(dir, ss_file_name)

    with open(ss_path, "rb") as f:
        res = spreadsheet_to_plan_list(
            spreadsheet_file=f, file_name=ss_file_name, data_type="wheel_xafs", user="User"
        )
        assert res == plan_list


# fmt: off
@pytest.mark.parametrize("ss_file_name", ["sample_ss_wheel_xafs_1.xlsx"])
# fmt: on
def test_spreadsheets_2(ss_file_name):
    dir = _get_sample_data_dir()
    ss_path = os.path.join(dir, ss_file_name)

    with open(ss_path, "rb") as f:
        with pytest.raises(Exception, match="Unsupported spreadsheet file"):
            fln_incorrect = ss_file_name + ".txt"
            spreadsheet_to_plan_list(
                spreadsheet_file=f, file_name=fln_incorrect, data_type="wheel_xafs", user="User"
            )

    with open(ss_path, "rb") as f:
        with pytest.raises(Exception, match="Data type .* is not supported"):
            spreadsheet_to_plan_list(
                spreadsheet_file=f, file_name=ss_file_name, data_type="incorrect", user="User"
            )
