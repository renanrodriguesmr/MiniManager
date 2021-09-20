#TODO: fix with new modes
import abc

class Configuration():
    id = 0
    medicao_schema = None
    measurements = [] # measurements
    mobility_model = None
    network = None # Network

class PropagationModel():
    established = False
    id = 0
    name = ''
    model = ''
    exp = 0

class Measurement():
    established = False
    frequency = 0
    measure = None # measure

class Measure():
    id = 0
    name = ''
    unit = ''

class PerformanceMeasure(Measure):
    source = ''
    destination = ''

class MobilityModel():
    established = False
    id = 0
    seed = 0
    model = ''
    min_velocidade = 0
    max_velocidade = 0
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_z = 0
    max_z = 0
    time = 0

class Network():
    established = False
    id = 0
    nodes = []
    controller = None
    noise_th = 0
    fading_cof = 0

class Controller():
    established = False
    id = 0
    protocolo = ''
    name = ''
    type = ''
    port = ''
    ip = ''

class NodeNetwork():
    established = False
    id = 0
    name = ''
    mac = ''
    authentication = None # Authentication
    hardware = None # Hardware
    mobility = None # Mobility
    position = None # Position

class Authentication():
    established = False
    user = ''
    password = ''
    type = ''

class Hardware():
    established = False
    id = 0
    core = 0
    cpu = 0

class Mobility():
    established = False
    id = 0
    time = 0
    position = None

class Position():
    x = 0
    y = 0
    z = 0

class Host(NodeNetwork):
    default_route = ''
    server = ''

class Switch(NodeNetwork):
    enable_cflow = False
    enable_netflow = False
    dpctlPort = 0
    type = ''
    dpid = ''
    server = ''

class Station(NodeNetwork):
    default_route = ''
    enable_netflow = False
    wlans = 0
    wpans = 0

class AcessPoint(NodeNetwork):
    enable_cflow = False
    enable_netflow = False
    dpctl_port = 0
    type = ''
    wlans = 0

class Interface():
    established = False
    id = 0
    name = ''
    ip = 0
    links = [] # Link
    protocol = None #Protocol

class Link():
    established = False
    connection = ''
    bandwith = 0
    delay = 0
    loss = 0
    max_queue_size = 0
    jitter = 0
    speedup = 0


class Protocol(abc.ABC):
    id = 0

class Wifi(Protocol):
    mode = ''
    ssid = ''
    channel = ''
