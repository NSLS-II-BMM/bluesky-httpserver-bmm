from .spreadsheets_base import BMMMacroBuilder


class WheelMacroBuilder(BMMMacroBuilder):
    """A class for parsing specially constructed spreadsheets and
    generating macros for measuring XAS on the BMM wheel.

    Examples
    --------
    >>> mb = MacroBuilder()
    >>> mb.spreadsheet('wheel1.xlsx')
    >>> mb.write_macro()
    """

    def _gen_plan_list(self):
        """Write a macro paragraph for each sample described in the
        spreadsheet.  A paragraph consists of line to move to the
        correct wheel slot, a line to change the edge energy (if
        needed), a line to measure the XAFS using the correct set of
        control parameters, and a line to close plot windows after the
        scan.

        Finally, write out the master INI and macro python files.
        """
        element, edge, focus = (None, None, None)
        for m in self.measurements:

            if m["default"] is True:
                element = m["element"]
                edge = m["edge"]
                continue
            if self.skip_row(m) is True:
                continue

            # default element/edge(/focus) values
            for k in ("element", "edge"):
                if m[k] is None:
                    m[k] = self.measurements[0][k]

            # sample and slit movement
            self.add_plan(name="slot", args=[m["slot"]])
            if m["samplex"] is not None:
                self.add_plan(name="mv", args=["xafs_x", m["samplex"]])
            if m["sampley"] is not None:
                self.add_plan(name="mv", args=["xafs_y", m["sampley"]])
            if m["slitwidth"] is not None:
                self.add_plan(name="mv", args=["slits3_hsize", m["slitwidth"]])
            if m["detectorx"] is not None:
                self.add_plan(name="mv", args=["xafs_det", m["detectorx"]])

            # change edge, if needed
            focus = False
            if m["focus"] == "focused":
                focus = True
            if self.do_first_change is True:
                self.add_plan(name="change_edge", args=[m["element"]], kwargs={"edge": m["edge"], "focus": focus})
                self.do_first_change = False
                self.totaltime += 4

            elif m["element"] != element or m["edge"] != edge:  # focus...
                element = m["element"]
                edge = m["edge"]
                self.add_plan(name="change_edge", args=[m["element"]], kwargs={"edge": m["edge"], "focus": focus})
                self.totaltime += 4

            # measure XAFS, then close all plots
            xafs_args = []
            xafs_kwargs = self.default_xafs_parameters.copy()
            command = self.tab + "yield from xafs('%s.ini'" % self.basename
            for k in m.keys():
                # skip cells with macro-building parameters that are not INI parameters
                if self.skip_keyword(k):
                    continue

                # skip element & edge if they are same as default
                elif k in ("element", "edge"):
                    if m[k] == self.measurements[0][k]:
                        continue

                # skip cells with only whitespace
                if type(m[k]) is str and len(m[k].strip()) == 0:
                    m[k] = None

                # if a cell has data, put it in the argument list for xafs()
                if m[k] is not None:
                    if k == "filename":
                        fname = self.make_filename(m)
                        xafs_kwargs["filename"] = fname
                    elif type(m[k]) is int:
                        command += ", %s=%d" % (k, m[k])
                        xafs_kwargs[k] = m[k]
                    elif type(m[k]) is float:
                        xafs_kwargs[k] = m[k]
                    else:
                        xafs_kwargs[k] = str(m[k])

            self.add_plan(name="xafs", args=xafs_args, kwargs=xafs_kwargs)

            # approximate time cost of this sample
            # self.estimate_time(m, element, edge)

        if self.close_shutters:
            self.add_plan(name="shb_close_plan")

    def get_keywords(self, row, defaultline):
        this = {
            "default": defaultline,
            "slot": row[1].value,  # sample location
            "measure": self.truefalse(row[2].value),  # filename and visualization
            "filename": row[3].value,
            "nscans": row[4].value,
            "start": row[5].value,
            "mode": row[6].value,
            # 'e0': row[7].value,
            "element": row[7 + self.offset].value,  # energy range
            "edge": row[8 + self.offset].value,
            "focus": row[9 + self.offset].value,
            "sample": row[10 + self.offset].value,  # scan metadata
            "prep": row[11 + self.offset].value,
            "comment": row[12 + self.offset].value,
            "bounds": row[13 + self.offset].value,  # scan parameters
            "steps": row[14 + self.offset].value,
            "times": row[15 + self.offset].value,
            "samplex": row[16 + self.offset].value,  # other motors
            "sampley": row[17 + self.offset].value,
            "slitwidth": row[18 + self.offset].value,
            "detectorx": row[19 + self.offset].value,
            "snapshots": self.truefalse(row[20 + self.offset].value),  # flags
            "htmlpage": self.truefalse(row[21 + self.offset].value),
            "usbstick": self.truefalse(row[22 + self.offset].value),
            "bothways": self.truefalse(row[23 + self.offset].value),
            "channelcut": self.truefalse(row[24 + self.offset].value),
            "ththth": self.truefalse(row[25 + self.offset].value),
            "url": row[26 + self.offset].value,
            "doi": row[27 + self.offset].value,
            "cif": row[28 + self.offset].value,
        }
        return this
