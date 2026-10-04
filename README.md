# Intelligent Elevator Controller

A Python-based elevator control system simulation with an interactive graphical interface.

## Overview

Intelligent Elevator Controller is a software simulation designed to model the operation of a multi-floor elevator system.

The application provides an interactive interface for requesting floors, managing elevator movement, processing requests, and monitoring system activity in real time.

Built entirely with Python and Tkinter, the project runs locally without external hardware or third-party packages.

## Features

- Multi-floor elevator simulation
- Interactive floor selection
- Automatic request queuing
- Elevator movement simulation
- Real-time system status monitoring
- Request processing and scheduling
- Data transfer simulation
- Memory access simulation
- System communication simulation
- System reset controls

## Architecture

```text
                         +----------------------+
                         |        USER          |
                         |  Floor Selection     |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |    INPUT / I/O       |
                         |   Floor Requests     |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |  CONTROLLER          |
                         | Request Processing   |
                         +----------+-----------+
                                    |
                         +----------v-----------+
                         |    REQUEST QUEUE     |
                         | Pending Floor Calls  |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |      ELEVATOR        |
                         | Movement Simulation  |
                         +----------------------+

        +----------------+       +----------------+
        |      DMA       | ----> |     MEMORY     |
        | Data Transfer  |       | Cache / RAM    |
        +-------+--------+       +----------------+
                |
                |
                v
        +-----------------------------------------+
        |              SYSTEM BUS                 |
        |   CPU / DMA / I/O Communication        |
        +-------------------+---------------------+
                            |
                            v
                  +---------------------+
                  |   BUS ARBITRATION   |
                  | Resource Selection  |
                  +---------------------+

```
## Technologies
- Python 3
- Tkinter
- Event-driven programming
## Requirements
- Python 3.x
- macOS, Windows, or Linux
- No external Python packages required
## Installation
Clone the repository:
git clone https://github.com/Britnyrifonykka2006/intelligent-elevator-controller.git

Navigate to the project directory:
cd intelligent-elevator-controller

## Running the Application
Run the following command:
python3 elevator_controller.py

The graphical interface will launch automatically.
## Project Structure
intelligent-elevator-controller/
|
├── elevator_controller.py
└── README.md

## Future Improvements
- Multiple elevator support
- Priority-based scheduling
- Emergency mode
- Door operation simulation
- Sensor integration
- Advanced scheduling algorithms
- Performance monitoring
## License
This project is provided for educational and demonstration purposes.
