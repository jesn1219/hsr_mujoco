import glfw
import mujoco_py
import numpy as np

import hsr
from hsr.util import add_env_args
from rl_utils import argparse, hierarchical_parse_args, space_to_size


class ControlViewer(mujoco_py.MjViewer):
    def __init__(self, sim):
        super().__init__(sim)
        self.active_joint = 0
        self.moving = False
        self.delta = None

        #Custom
        self.action_num = 0

    def key_callback(self, window, key, scancode, action, mods):
        super().key_callback(window, key, scancode, action, mods)
        keys = [
            glfw.KEY_0,
            glfw.KEY_1,
            glfw.KEY_2,
            glfw.KEY_3,
            glfw.KEY_4,
            glfw.KEY_5,
            glfw.KEY_6,
            glfw.KEY_7,
            glfw.KEY_8,
            glfw.KEY_9,
        ]
        if key in keys:
            self.active_joint = keys.index(key)
            #print(self.sim.model.joint_names[self.active_joint])

        if key == glfw.KEY_UP and action == glfw.PRESS:
            if self.delta != None :
                self.delta += 0.1
            else : 
                self.delta = 0
            print("self.delta : {}".format(self.delta))
        if key == glfw.KEY_DOWN and action == glfw.PRESS:
            if self.delta  != None:
                self.delta -= 0.1
            else : 
                self.delta = 0
            print("self.delta : {}".format(self.delta))
        if key == glfw.KEY_RIGHT and action == glfw.PRESS:
            self.action_num += 1
            self.active_joint = self.action_num
            print("action_num : {}".format(self.action_num))

        if key == glfw.KEY_LEFT and action == glfw.PRESS:
            self.action_num -= 1
            self.active_joint = self.action_num
            print("action_num : {}".format(self.action_num))

        elif key == glfw.KEY_LEFT_CONTROL and action == glfw.PRESS:
            self.moving = not self.moving

            self.delta = None
            print("self.moving : {}".format(self.moving))

    def _cursor_pos_callback(self, window, xpos, ypos):
        super()._cursor_pos_callback(window, xpos, ypos)
        '''
        if self.moving:
            self.delta = self._last_mouse_y - int(self._scale * ypos)
        '''


class ControlHSREnv(hsr.HSREnv):
    def viewer_setup(self):
        self.viewer = ControlViewer(self.sim)

    def control_agent(self):
        action = np.zeros(space_to_size(self.action_space))
        action_scale = np.ones_like(action)
        # action_scale[[0, 1]] = .1
        # action[3] = 100
        if self.viewer and self.viewer.moving:
            print('delta =', self.viewer.delta)
        if self.viewer and self.viewer.moving and self.viewer.delta:
            # jesnk : code below necessary?
            action[self.viewer.active_joint] = self.viewer.delta

            # if self.sim.model.joint_names[self.viewer.active_joint] == 'l_proximal_joint':
            #     if action[self.sim.model.get_]
            print('delta =', self.viewer.delta)
            print('action =', action)

        s, r, t, i = self.step(action * action_scale)
        return t


def main(env_args):
    env = ControlHSREnv(**env_args)
    done = False

    action = np.zeros(space_to_size(env.action_space))
    action[0] = 1

    while True:
        if done:
            env.reset()
        done = env.control_agent()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    wrapper_parser = parser.add_argument_group('wrapper_args')
    env_parser = parser.add_argument_group('env_args')
    hsr.util.add_env_args(env_parser)
    hsr.util.add_wrapper_args(wrapper_parser)
    args = hierarchical_parse_args(parser)
    main_ = hsr.util.env_wrapper(main)(**args)
