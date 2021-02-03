source ../venv/bin/activate
python hsr/control.py \
    --block-space '(0,0)(0,0)(0,0)(0,0)' \
    --steps-per-action=300 \
    --geofence=.5 \
    --goal-space '(0,0)(0,0)(0,0)' \
    --use-dof slide_x \
    --use-dof slide_y \
    --use-dof torso_lift_joint \
    --use-dof head_pan_joint \
    --use-dof head_tilt_joint \
    --use-dof arm_flex_joint \
    --use-dof arm_roll_joint \
    --use-dof wrist_flex_joint \
    --use-dof wrist_roll_joint \
    --use-dof head_motor_joint \
    --use-dof hand_l_proximal_joint \
    --use-dof hand_l_spring_proximal_joint \
    --use-dof hand_l_mimic_distal_joint
    --use-dof hand_l_distal_joint \
    --use-dof hand_r_proximal_joint \
    --use-dof hand_r_spring_proximal_joint \
    --use-dof hand_r_mimic_distal_joint
    --use-dof hand_r_distal_joint \

    --render

