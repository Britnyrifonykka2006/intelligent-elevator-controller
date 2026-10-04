import tkinter as tk

# ============================================================
# INTELLIGENT ELEVATOR CONTROLLER
# COMPUTER ORGANIZATION & ARCHITECTURE - UNIT 5
#
# I/O + INTERRUPTS + REQUEST QUEUE
# DMA + CACHE + RAM
# SYSTEM BUS + BUS ARBITRATION
# ============================================================

root = tk.Tk()
root.title("Intelligent Elevator Controller - COA")
root.geometry("1000x870")
root.configure(bg="#111111")
root.resizable(False, False)


# ============================================================
# VARIABLES
# ============================================================

current_floor = 1
request_queue = []

interrupt_count = 0
moving = False

# DMA
dma_active = False
dma_progress = 0
dma_transfers = 0

# CACHE / RAM
cache = []
cache_size = 3
cache_hits = 0
cache_misses = 0
ram_accesses = 0

# BUS
bus_busy = False
bus_granted_to = "NONE"
bus_transfers = 0


floor_y = {
    1: 570,
    2: 470,
    3: 370,
    4: 270,
    5: 170
}


# ============================================================
# HELPER
# ============================================================

def make_button(text, x, y, width=25, height=2,
                command=None, bg="#292629", font=("Arial", 11)):
    button = tk.Button(
        root,
        text=text,
        width=width,
        height=height,
        bg=bg,
        fg="#ffffff",
        activebackground="#444044",
        activeforeground="#ffffff",
        relief="flat",
        font=font,
        command=command
    )
    button.place(x=x, y=y)
    return button


# ============================================================
# FLOOR STATUS
# ============================================================

def update_status():
    status_button.config(
        text="CURRENT FLOOR: " + str(current_floor)
    )


# ============================================================
# BUS ARBITRATION
# ============================================================

def request_bus(device):

    global bus_busy
    global bus_granted_to
    global bus_transfers

    if bus_busy:
        bus_request_button.config(
            text="BUS BUSY: " + bus_granted_to
        )
        return

    bus_busy = True
    bus_granted_to = device
    bus_transfers += 1

    bus_request_button.config(
        text="BUS REQUEST: " + device
    )

    bus_grant_button.config(
        text="BUS GRANTED TO: " + device
    )

    bus_status_button.config(
        text="SYSTEM BUS: BUSY"
    )

    bus_count_button.config(
        text="BUS TRANSFERS: " + str(bus_transfers)
    )

    root.after(800, release_bus)


def release_bus():

    global bus_busy
    global bus_granted_to

    bus_busy = False
    bus_granted_to = "NONE"

    bus_status_button.config(
        text="SYSTEM BUS: IDLE"
    )

    bus_request_button.config(
        text="BUS REQUEST: NONE"
    )

    bus_grant_button.config(
        text="BUS GRANTED TO: NONE"
    )


# ============================================================
# CACHE + RAM
# ============================================================

def access_memory(floor):

    global cache_hits
    global cache_misses
    global ram_accesses

    request_bus("CPU")

    if floor in cache:

        cache_hits += 1

        cache_status_button.config(
            text="CACHE: HIT"
        )

    else:

        cache_misses += 1
        ram_accesses += 1

        cache_status_button.config(
            text="CACHE: MISS -> RAM"
        )

        if len(cache) >= cache_size:
            cache.pop(0)

        cache.append(floor)

    update_memory_display()


def update_memory_display():

    cache_button.config(
        text="CACHE CONTENT: " + str(cache)
    )

    cache_hits_button.config(
        text="CACHE HITS: " + str(cache_hits)
    )

    cache_misses_button.config(
        text="CACHE MISSES: " + str(cache_misses)
    )

    ram_button.config(
        text="RAM ACCESSES: " + str(ram_accesses)
    )


# ============================================================
# I/O FLOOR REQUEST
# ============================================================

def request_floor(floor):

    global interrupt_count

    # I/O requests the bus
    request_bus("I/O")

    # Generate interrupt
    interrupt_count += 1

    interrupt_button.config(
        text="INTERRUPTS: " + str(interrupt_count)
    )

    # CPU accesses memory
    access_memory(floor)

    if floor not in request_queue and floor != current_floor:
        request_queue.append(floor)

    queue_button.config(
        text="REQUEST QUEUE: " + str(request_queue)
    )

    process_queue()


# ============================================================
# REQUEST QUEUE
# ============================================================

def process_queue():

    global moving

    if moving:
        return

    if len(request_queue) == 0:

        controller_button.config(
            text="CPU / CONTROLLER: IDLE"
        )

        return

    next_floor = request_queue.pop(0)

    queue_button.config(
        text="REQUEST QUEUE: " + str(request_queue)
    )

    controller_button.config(
        text="CPU / CONTROLLER: PROCESSING"
    )

    request_bus("CPU")

    move_elevator(next_floor)


# ============================================================
# ELEVATOR MOVEMENT
# ============================================================

def move_elevator(target_floor):

    global current_floor
    global moving

    moving = True

    if current_floor < target_floor:
        current_floor += 1

    elif current_floor > target_floor:
        current_floor -= 1

    else:

        moving = False
        process_queue()
        return

    elevator_button.place(
        x=185,
        y=floor_y[current_floor]
    )

    update_status()

    root.after(
        500,
        lambda: move_elevator(target_floor)
    )


# ============================================================
# DMA
# ============================================================

def start_dma():

    global dma_active
    global dma_progress

    if dma_active:
        return

    request_bus("DMA")

    dma_active = True
    dma_progress = 0

    dma_status_button.config(
        text="DMA TRANSFER: 0%"
    )

    dma_info_button.config(
        text="DMA: SENSOR DATA -> RAM"
    )

    dma_step()


def dma_step():

    global dma_progress
    global dma_active
    global dma_transfers

    if not dma_active:
        return

    dma_progress += 20

    dma_status_button.config(
        text="DMA TRANSFER: " + str(dma_progress) + "%"
    )

    if dma_progress < 100:

        root.after(300, dma_step)

    else:

        dma_active = False
        dma_transfers += 1

        dma_status_button.config(
            text="DMA TRANSFER COMPLETE"
        )

        dma_info_button.config(
            text="DMA: DATA -> RAM"
        )

        dma_count_button.config(
            text="DMA TRANSFERS: " + str(dma_transfers)
        )


# ============================================================
# RESET
# ============================================================

def reset_system():

    global current_floor
    global request_queue
    global interrupt_count
    global moving

    global dma_active
    global dma_progress
    global dma_transfers

    global cache
    global cache_hits
    global cache_misses
    global ram_accesses

    global bus_busy
    global bus_granted_to
    global bus_transfers

    current_floor = 1
    request_queue = []
    interrupt_count = 0
    moving = False

    dma_active = False
    dma_progress = 0
    dma_transfers = 0

    cache = []
    cache_hits = 0
    cache_misses = 0
    ram_accesses = 0

    bus_busy = False
    bus_granted_to = "NONE"
    bus_transfers = 0

    elevator_button.place(
        x=185,
        y=floor_y[1]
    )

    update_status()

    controller_button.config(
        text="CPU / CONTROLLER: IDLE"
    )

    interrupt_button.config(
        text="INTERRUPTS: 0"
    )

    queue_button.config(
        text="REQUEST QUEUE: []"
    )

    dma_status_button.config(
        text="DMA STATUS: IDLE"
    )

    dma_info_button.config(
        text="DMA: READY"
    )

    dma_count_button.config(
        text="DMA TRANSFERS: 0"
    )

    cache_status_button.config(
        text="CACHE: READY"
    )

    update_memory_display()

    bus_status_button.config(
        text="SYSTEM BUS: IDLE"
    )

    bus_request_button.config(
        text="BUS REQUEST: NONE"
    )

    bus_grant_button.config(
        text="BUS GRANTED TO: NONE"
    )

    bus_count_button.config(
        text="BUS TRANSFERS: 0"
    )


# ============================================================
# FINAL CLEAN GUI
# ============================================================

# ============================================================
# TITLE
# ============================================================

title_button = make_button(
    "INTELLIGENT ELEVATOR CONTROLLER",
    250, 20,
    width=50,
    height=2,
    bg="#252225",
    font=("Arial", 19, "bold")
)


# ============================================================
# LEFT - ELEVATOR
# ============================================================

elevator_section = make_button(
    "ELEVATOR SYSTEM",
    60, 100,
    width=35,
    height=2,
    bg="#302d30",
    font=("Arial", 13, "bold")
)

floor_y = {
    5: 170,
    4: 235,
    3: 300,
    2: 365,
    1: 430
}

for floor in range(5, 0, -1):

    make_button(
        "FLOOR " + str(floor),
        80,
        floor_y[floor],
        width=12,
        height=2
    )

elevator_button = make_button(
    "ELEVATOR",
    240,
    floor_y[1],
    width=14,
    height=2,
    bg="#3b373b",
    font=("Arial", 11, "bold")
)


# ============================================================
# LEFT - I/O REQUESTS
# ============================================================

io_section = make_button(
    "I/O FLOOR REQUESTS",
    60, 500,
    width=35,
    height=2,
    bg="#302d30",
    font=("Arial", 12, "bold")
)

for i in range(1, 6):

    make_button(
        "REQUEST " + str(i),
        45 + ((i - 1) * 78),
        540,
        width=9,
        height=2,
        bg="#363236",
        command=lambda floor=i: request_floor(floor)
    )


# ============================================================
# LEFT - BUS ARBITRATION
# ============================================================

bus_section = make_button(
    "BUS ARBITRATION",
    60, 590,
    width=35,
    height=2,
    bg="#302d30",
    font=("Arial", 12, "bold")
)

cpu_bus_button = make_button(
    "CPU BUS",
    60, 630,
    width=9,
    command=lambda: request_bus("CPU")
)

dma_bus_button = make_button(
    "DMA BUS",
    165, 630,
    width=9,
    command=lambda: request_bus("DMA")
)

io_bus_button = make_button(
    "I/O BUS",
    270, 630,
    width=9,
    command=lambda: request_bus("I/O")
)

bus_status_button = make_button(
    "SYSTEM BUS: IDLE",
    60, 670,
    width=35
)

bus_request_button = make_button(
    "BUS REQUEST: NONE",
    60, 710,
    width=35
)

bus_grant_button = make_button(
    "BUS GRANTED TO: NONE",
    60, 750,
    width=35
)

bus_count_button = make_button(
    "BUS TRANSFERS: 0",
    60, 790,
    width=17
)

reset_button = make_button(
    "RESET SYSTEM",
    265, 790,
    width=17,
    bg="#363236",
    command=reset_system
)


# ============================================================
# RIGHT - SYSTEM STATUS
# ============================================================

system_section = make_button(
    "SYSTEM STATUS",
    540, 100,
    width=40,
    height=2,
    bg="#302d30",
    font=("Arial", 13, "bold")
)

status_button = make_button(
    "CURRENT FLOOR: 1",
    540, 145,
    width=40
)

controller_button = make_button(
    "CPU / CONTROLLER: IDLE",
    540, 185,
    width=40
)

interrupt_button = make_button(
    "INTERRUPTS: 0",
    540, 225,
    width=40
)

queue_button = make_button(
    "REQUEST QUEUE: []",
    540, 265,
    width=40
)


# ============================================================
# RIGHT - DMA
# ============================================================

dma_section = make_button(
    "DMA CONTROLLER",
    540, 310,
    width=40,
    height=2,
    bg="#302d30",
    font=("Arial", 13, "bold")
)

dma_status_button = make_button(
    "DMA STATUS: IDLE",
    540, 355,
    width=40
)

dma_info_button = make_button(
    "DMA: READY",
    540, 395,
    width=40
)

dma_count_button = make_button(
    "DMA TRANSFERS: 0",
    540, 435,
    width=40
)

start_dma_button = make_button(
    "START DMA TRANSFER",
    540, 475,
    width=40,
    bg="#363236",
    command=start_dma
)


# ============================================================
# RIGHT - MEMORY
# ============================================================

memory_section = make_button(
    "MEMORY SYSTEM",
    540, 520,
    width=40,
    height=2,
    bg="#302d30",
    font=("Arial", 13, "bold")
)

cache_status_button = make_button(
    "CACHE: READY",
    540, 560,
    width=40
)

cache_button = make_button(
    "CACHE CONTENT: []",
    540, 600,
    width=40
)

cache_hits_button = make_button(
    "CACHE HITS: 0",
    540, 640,
    width=40
)

cache_misses_button = make_button(
    "CACHE MISSES: 0",
    540, 680,
    width=40
)

ram_button = make_button(
    "RAM ACCESSES: 0",
    540, 720,
    width=40
)


# ============================================================
# START
# ============================================================

root.mainloop()