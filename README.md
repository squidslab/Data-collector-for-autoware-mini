# Autoware mini data collector

## Description

This script collects data by listening to Autoware Mini topics. The README explains how to start CARLA and launch Autoware Mini with the Scenario Runner.

## Requirements

- Follow the installation procedure specified in the Autoware Mini GitHub repository (https://github.com/Autoware-AI/autoware_mini)

## Starting CARLA

Run the following command from the CARLA root directory:

```bash
$CARLA_ROOT/CarlaUE4.sh
```

This starts the CARLA simulator.

## Launching Autoware Mini with Scenario Runner

After starting CARLA, open a new terminal and run the following command to launch Autoware Mini:

```bash
roslaunch autoware_mini start_carla.launch use_scenario_runner:=true
```

### Map selection

You can specify the map with the `map_name` parameter:

```bash
roslaunch autoware_mini start_carla.launch map_name:=Town01 use_scenario_runner:=true
```

or:

```bash
roslaunch autoware_mini start_carla.launch map_name:=Town04 use_scenario_runner:=true
```

If `map_name` is not specified, the default map `tartu_demo` is launched.

## Scenario Runner

The Scenario Runner allows selecting and running test scenarios using `.xosc` files via Autoware Mini's interface.

Scenario files are located in the Autoware Mini repository, typically under:

```text
data/scenarios/MAP_NAME/SCENARIO_NAME.xosc
```

## Notes

- Ensure that CARLA and Autoware Mini are compatible with each other.
- Check the ROS version and the packages required by Autoware Mini.
- If launching the Scenario Runner does not work, verify environment variables and the paths to the `.xosc` files.

## Useful resources

- Autoware Mini repository: https://github.com/Autoware-AI/autoware_mini
- CARLA documentation: https://carla.org/

