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


###############################################################################
# The following code has been copy and pasted from the "exploration" document #
# Reference that for comments/documentation ###################################
###############################################################################


client = carla.Client("localhost", 2000)
world = client.get_world()

vehicle_bp = world.get_blueprint_library().filter("*vehicle*")
spawn_points = world.get_map().get_spawn_points()

test_vehicle_bp = world.get_blueprint_library().filter("vehicle.audi.tt")[0]
test_spawn_point = spawn_points[0]
test_vehicle = world.spawn_actor(test_vehicle_bp, test_spawn_point)

for i in range(20):
    vehicle = random.choice(vehicle_bp)
    location = random.choice(spawn_points)
    world.try_spawn_actor(vehicle, location)

spectator = world.get_actors().filter("spectator")[0]
spectator.set_transform(carla.Transform(
    test_vehicle.get_transform().location + carla.Location(x=11, z=4),
    carla.Rotation(
        pitch=test_vehicle.get_transform().rotation.pitch - 13,
        yaw=test_vehicle.get_transform().rotation.yaw - 180
    )))

relative_offset = carla.Location(x=0.7, z=1.75)
camera_transform = carla.Transform(relative_offset, test_vehicle.get_transform().rotation)
camera_bp = world.get_blueprint_library().find("sensor.camera.rgb")
camera = world.spawn_actor(camera_bp, camera_transform, attach_to=test_vehicle)

for vehicle in world.get_actors().filter("*vehicle*"):
    vehicle.set_autopilot(True)

camera.listen(lambda image: image.save_to_disk("data_output/%06d.png" % image.frame))
time.sleep(30)

for vehicle in world.get_actors().filter("*vehicle*"):
    vehicle.destroy()

camera.destroy()

print("All sensors and vehicles have been destoryed")
print("Program ran successfully, quitting now")