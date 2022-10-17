from os import TMP_MAX
from socket import *

class SocketConnect():
    ALTI_socket        = socket(AF_INET, SOCK_DGRAM) # Multicast socket
    DEPTH_socket       = socket(AF_INET, SOCK_DGRAM) # Multicast socket
    DVL_socket         = socket(AF_INET, SOCK_DGRAM) # Multicast socket
    R1_OP_socket       = socket(AF_INET, SOCK_DGRAM) # Broadcast socket
    ALTI_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    DEPTH_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    DVL_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

class ALTI():
    ip                 = "239.0.1.44"
    port               = 62441
    Data               = 0

class DEPTH():
    ip                 = "239.0.1.44"
    port               = 62442
    Data               = 0

class R1_OP():
    ip                 = "" # Broadcast socket
    port               = 60880
    Zone               = 52
    Data               = 0

class DVL():
    ip                 = "239.0.1.46"
    port               = 62461
    Data               = 0
    system_config      = 0
    velBtm_x           = 0
    velBtm_y           = 0
    velBtm_z           = 0
    velBtm_e           = 0
    velRef_x           = 0
    velRef_y           = 0
    velRef_z           = 0
    velRef_e           = 0
    beam1              = 0
    beam2              = 0
    beam3              = 0
    beam4              = 0
    sound_speed        = 0
    temperature        = 0
    salinity           = 0
    depth              = 0
    roll               = 0
    pitch              = 0
    heading            = 0
    velocity           = 0
    altimeter          = 0 

class lists():
    m_adOutput         = [0 for i in range(88)]
    real_data          = []
    int_bin_data       = []
    int_bin_alt        = []
    spl_list           = []
    real_data_depth    = []
    real_data_alt      = []
    graph_X            = []
    graph_Y            = []
    graph_test         = [i for i in range(10)]

class PSIMSSB():
    rov_Beacon         = 0
    rov_coordinateX    = 0
    rov_coordinateY    = 0
    rov_depth          = 0

    tms_Beacon         = 0
    tms_coordinateX    = 0
    tms_coordinateY    = 0
    tms_depth          = 0

    ship_Beacon        = 0
    ship_coordinateX   = 0
    ship_coordinateY   = 0
    ship_depth         = 0

class PSIMSNS():
    rov_Roll           = 0
    rov_Pitch          = 0
    rov_Heave          = 0
    rov_Heading        = 0
    
    tms_Roll           = 0
    tms_Pitch          = 0
    tms_Heave          = 0
    tms_Heading        = 0

    ship_Roll          = 0
    ship_Pitch         = 0
    ship_Heave         = 0
    ship_Heading       = 0

class INGLL():
    rov_latDeg         = 0
    rov_lonDeg         = 0
    rov_UTM_X          = 0
    rov_UTM_Y          = 0

    tms_latDeg         = 0
    tms_lonDeg         = 0
    tms_UTM_X          = 0
    tms_UTM_Y          = 0

    ship_latDeg        = 0
    ship_lonDeg        = 0
    ship_UTM_X         = 0
    ship_UTM_Y         = 0

class ShipGPS():
    Lat                = 0
    Lon                = 0
    Sat                = 0
    Heading            = 0

class NaviData():
    TmpData            = 0
    RawDataBrowser     = 0
    TimeBrowser        = 0
    LatBrowser         = 0
    LonBrowser         = 0
    DepthBrowser       = 0
    AltiBrowser        = 0
    EventInputEdit     = 0
    
    ListNaviData       = [0]*6
    EventData          = 0