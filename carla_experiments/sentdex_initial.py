import sys
# Need this for file control so programs can be developed outside of the installation path
# Need this for file control so programs can be developed outside of the installation path
f_path = r"C:\Users\mikel\Downloads\Other Important Things\RWTH-Aachen Stuff\Indpendent_Study\carla_driving_sim_work\carla\dist\carla-0.9.15-py3.7-win-amd64.egg"

agent_path = r"C:\Users\mikel\Downloads\Other Important Things\RWTH-Aachen Stuff\Indpendent_Study\carla_driving_sim_work\carla"

sys.path.append(f_path)
sys.path.append(agent_path)

import carla
import random
import time
import numpy as np
import cv2


###############################################################################
# Following along with the development from sentdex (initial script based)#####
###############################################################################

IM_WIDTH = 640
IM_HEIGHT = 480

def process_img(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return i3/255.0

actor_list = []

try:
    client = carla.Client("localhost", 2000)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    vehicle_bp = blueprint_library.filter("model3")[0]
    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    vehicle.set_autopilot(True)
    actor_list.append(vehicle)

    camera_bp = blueprint_library.find("sensor.camera.rgb")
    camera_bp.set_attribute("image_size_x", f"{IM_WIDTH}")
    camera_bp.set_attribute("image_size_y", f"{IM_HEIGHT}")
    camera_bp.set_attribute("fov", "110")

    cam_spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    camera = world.spawn_actor(camera_bp, cam_spawn_point, attach_to=vehicle)
    actor_list.append(camera)
    camera.listen(lambda data: process_img(data))


    time.sleep(5)

finally:
    for actor in actor_list:
        actor.destroy()
    print("All actors are cleaned up")