cmds.select('lf_knee_PV', 'rt_knee_PV', r = True)
    cmds.group(name = 'knee_PV_CTRLGRP')
    cmds.parentConstraint('root_CTRL', 'knee_PV_CTRLGRP', mo = True)