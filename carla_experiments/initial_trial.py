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


client = carla.Client("localhost", 2000)
world = client.get_world()

vehicle_bp = world.get_blueprint_library().filter("*vehicle*")
spawn_points = world.get_map().get_spawn_points()

for i in range(0,20):
    vehicle = random.choice(vehicle_bp)
    location = random.choice(spawn_points)
    world.try_spawn_actor(vehicle, location)

# set all of the vehicels on autopilot
for vehicle in world.get_actors().filter('*vehicle*'):
    vehicle.set_autopilot(True)

# allow the program to run for 10 seconds
time.sleep(10)

# destory the vehicles
for vehicle in world.get_actors().filter('*vehicle*'):
    vehicle.destroy()

print("The program has ran successfully, qutting now.")