def create_arm_stretchy_ik(s):
    #    make locators
    cmds.spaceLocator(name='shoulder_dist')
    cmds.spaceLocator(name='control_dist')
    cmds.pointConstraint('ik_lf_shoulder_JNT', 'shoulder_dist')
    cmds.pointConstraint('ik_lf_wrist_CTRL', 'control_dist')
    #    determine distance
    measure_startX = cmds.getAttr('shoulder_dist.translateX')
    measure_startY = cmds.getAttr('shoulder_dist.translateY')
    measure_startZ = cmds.getAttr('shoulder_dist.translateZ')
    measure_endX = cmds.getAttr('control_dist.translateX')
    measure_endY = cmds.getAttr('control_dist.translateY')
    measure_endZ = cmds.getAttr('control_dist.translateZ')
    cmds.distanceDimension(sp=(measure_startX, measure_startY, measure_startZ), ep=(measure_endX, measure_endY, measure_endZ))
    initial_distance_value = cmds.getAttr('distanceDimensionShape1.distance')
    cmds.spaceLocator(name="intial_dist")
    cmds.addAttr(at="float", sn="intial_distance", k=True, w=True, r=True, dv=initial_distance_value)
    #    create boolean attr in ik control to turn stretchy on and off
    cmds.select("ik_lf_wrist_CTRL", r=True)
    cmds.addAttr(at='bool', sn="stretchy_ik", k=True, w=True, r=True, dv=0)
    #    create expression
    cmds.expression(s="float $distance = distanceDimensionShape1.distance; float $initial_distance = `getAttr distanceDimensionShape1.distance`; float $factor = $distance/$initial_distance; ik_lf_shoulder_JNT.scaleX = $factor; ik_lf_elbow_JNT.scaleX = $factor;", n="lf_arm_stretchy_ik", o=" ", ae=1, uc="all")