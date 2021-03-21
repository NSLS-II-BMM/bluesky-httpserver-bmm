from .spreadsheets_wheel_xafs import WheelMacroBuilder


def spreadsheet_to_plan_list(*, spreadsheet_file, file_name, data_type, user, **kwargs):
    """
    Convert spreadsheet into a list of plans that could be added to the queue.

    Parameters
    ----------
    spreadsheet_file : file
        Readable file object.
    file_name : str
        The name of uploaded spreadsheet file.
    data_type : str, None
        Data type, such as ``excel``. May be used to select proper processing function.
    user : str
        User name: may be used as part of plan parameters.

    Returns
    -------
    plan_list : list(dict)
        Dictionary representing a list of plans extracted from the spreadsheet.
    """
    import os

    supported_extensions = (".xlsx", ".xlsm", ".xltx", ".xltm")
    ext = os.path.splitext(file_name)[1]
    if ext not in supported_extensions:
        raise ValueError(
            f"Unsupported spreadsheet file '{file_name}' (extension '{ext}'). "
            f"Only extensions {supported_extensions} are supported"
        )

    if data_type and (data_type.lower() == "wheel_xafs"):
        mb = WheelMacroBuilder(user_name=user)
        return mb.process_spreadsheet(spreadsheet_file=spreadsheet_file, energy=True)
    else:
        raise ValueError(f"Data type '{data_type}' is not supported.")
