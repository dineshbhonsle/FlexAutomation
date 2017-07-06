#!/usr/bin/python
#This file reads the testbed file and checks if the described topology is docker or a harware setup. If it is a
#docker setup, it instantiates docker instances based on the details from the testbed.json file and also creates
#links, ports and connects them to the docker. Just execute this file as any Python module.

import json, re, time
import subprocess, os, signal, sys, traceback
import threading
from robot.api import logger


MAX_DEVICE_COUNT = 32
MAX_THREADS = 16
docker_image = "snapos/flex:latest"
netns_dir = "/var/run/netns/"
device_name_reg = "^[a-zA-Z0-9\-\._]{2,64}$"
link_name_reg = "^(fpPort[0-9]{1,4})$"
link_state_reg = "^[0-9]+:[ ]*(?P<intf>[^@:]+)(@[^:]+)?:"
common_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
testBed_path = sys.argv[1]
Device = "Device"
Links = "Links"
mgmtIP = "mgmtIP"
device_ports = "ports"
Interface = "Intf"



def pretty_print(js):
    """ try to convert json to pretty-print format """
    try:
        return json.dumps(js, indent=4, separators=(",", ":"), sort_keys=True)
    except Exception as e:
        return "%s" % js

def exec_cmd(cmd, ignore_exception=False):
    """ execute command and return stdout output - None on error """
    try:
        logger.debug("excecuting command: %s" % cmd)
        out = subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT)
        return out
    except subprocess.CalledProcessError as e:
        # exit code -2 seen on ctrl+c interrupt
        if e.returncode < 0: sys.exit("\nExiting...\n")
        if ignore_exception: 
            logger.debug("error executing cmd: %s" % e)
            logger.debug("stderr: %s" % e.output)
            return None
        logger.warn("error executing cmd: %s" % cmd)
        logger.warn("%s" % e.output)
        raise e

def buildTopoFile(topology_file):

    try:
        topo = {"devices" : [],"connections" :[]}
        with open(topology_file, "r") as f: js = json.load(f)
        devices = {}
        devList = js[Device].keys()
        linkList =js[Links].keys()
        port_start = "8001"
        for device in sorted(devList):
            topo["devices"].append({"name" : device, "port" : str(port_start)})
            port_start = int(port_start) + 1  
            
        for link in sorted(linkList):
         
            connectedDevice = js[Links][link].keys()
            port1 = js[Links][link][connectedDevice[0]][Interface]
            port2 = js[Links][link][connectedDevice[1]][Interface]
            dev1 = js[Device][connectedDevice[0]][device_ports][port1]
            dev2 = js[Device][connectedDevice[1]][device_ports][port2]
            topo["connections"].append({connectedDevice[0] : dev1,connectedDevice[1] : dev2})
       
   	return topo

    except IOError as e:
        logger.error("failed to open topology json file: %s" % (
            topology_file))
        return None
    except ValueError as e:
        logger.error("failed to parse topology json file: %s" % (
            topology_file))
        return None


def get_topology(topology_file = None):
    """ read in topology file, verify connections, and return new topology 
        dict in the following 
        format:
            "devices":{
                "device_name":{
                    "port":"",  # docker exposed port
                    "pid":"",   # docker pid once created
                    "connections": [
                        {"local-port":"","remote-device":"","remote-port":""}
                    ],
                    "interfaces": [] # list of interface names
                }
            }
        Note, the device with the lower name will record the connection so
        it's possible to have devices created with no connections
        (as 'remote' connection is in connection list of a different device)
    
        a valid topology_file must meet the following requirements:
            * between 2 and max_device_count devices
            * no duplicate links on any device
            * eth0 cannot be used on any link
            * no 'loopback' connections to the same device
    """
    try:
        #with open(topology_file, "r") as f: js = json.load(f)
        js = buildTopoFile(topology_file)
        devices = {}
        for attr in ["devices", "connections"]:
            if attr not in js or len(js[attr]) == 0 or \
                type(js[attr]) is not list:
                em = "invalid topology file. Expect '%s' attribute " % attr
                em+= "with type 'list' and length>0"
                logger.error(em)
                return None
        # build device list first
        for d in js["devices"]:
            if type(d) is not dict or "name" not in d or "port" not in d:
                logger.error("invalid device object: %s" % d)
                return None
            if not re.search(device_name_reg, d["name"]):
                logger.error("invalid device name '%s'" % dn)
                return None
            try:
                port = int(d["port"])
                if port >= 0xffff or port < 0x400:
                    logger.error("invalid port %s, must be between %d and %d"%(
                        port, 0x400, 0xffff))
                    return None
            except ValueError as e:
                logger.error("invalid port for %s, must be an integer" % d)
                return None
            # everything ok, add to devices
            devices[d["name"].lower()] = {
                    "name": d["name"], "port": int(d["port"]),
                    "connections": [], "interfaces":[], "pid":""
            }

        # build connections
        for c in js["connections"]:
            if type(c) is not dict or len(c.keys())!=2 or \
                (type(c[c.keys()[0]]) is not str and \
                type(c[c.keys()[0]]) is not unicode) or \
                len(c[c.keys()[0]])==0 or \
                (type(c[c.keys()[1]]) is not str and \
                type(c[c.keys()[1]]) is not unicode) or \
                len(c[c.keys()[1]])==0:
                logger.error("invalid connection: %s" % c)
                return None
            # verify device name and connection name
            d1,c1 = (c.keys()[0], c[c.keys()[0]])
            d2,c2 = (c.keys()[1], c[c.keys()[1]])
            d1_lower, d2_lower = (d1.lower(), d2.lower())
            if d1_lower not in devices:
                logger.error("device %s not in devices list" % d1_lower)
                return None
            if d2_lower not in devices:
                logger.error("device %s not in devices list" % d2_lower)
                return None
            for cn in (c1, c2):
                if not re.search(link_name_reg, cn):
                    logger.error("invalid connection name '%s'" % cn)
                    return None
            if d1_lower == d2_lower:
                logger.error("unsupported back-to-back connection: %s" % c)
                return None
            if c1 == "eth0" or c2 == "eth0":
                logger.error("eth0 is reserved for docker management: %s" % c)
                return None
            if c1 in devices[d1_lower]["interfaces"]:
                em = "device %s interface %s referenced multiple times" % (
                    d1_lower, c1)
                logger.error(em)
                return None
            if c2 in devices[d2_lower]["interfaces"]:
                em = "device %s interface %s referenced multiple times" % (
                    d2_lower, c2)
                logger.error(em)
                return None
            devices[d1_lower]["interfaces"].append(c1)
            devices[d2_lower]["interfaces"].append(c2)
            if d1_lower <= d2_lower:
                devices[d1_lower]["connections"].append({
                    "local-port":c1, "remote-port":c2,
                    "remote-device":d2_lower
                })
            else:
                devices[d2_lower]["connections"].append({
                    "local-port":c2, "remote-port":c1,
                    "remote-device":d1_lower
                })
    except IOError as e:
        logger.error("failed to open topology json file: %s" % (
            topology_file))
        return None
    except ValueError as e:
        logger.error("failed to parse topology json file: %s" % (
            topology_file))
        return None

    if len(devices) > MAX_DEVICE_COUNT:
        logger.error("Number of devices (%s) exceeds maximum count %s" % (
            len(devices), MAX_DEVICE_COUNT))
        return None
    elif len(devices) == 0:
        logger.error("No valid devices found in topology file")
        return None
    
    return devices


def check_docker_running():
    """ check if docker is running/successfully connect to it 
        return boolean success
    """
    logger.info("checking docker state")
    out = exec_cmd("docker ps", ignore_exception=True)
    return (out is not None)

def check_docker_image():
    """ check if docker_image is present.  If not, print info message and
        pull it down
    """
    img = docker_image.split(":")
    if len(img) == 2:
        if len(img[0]) == 0 or len(img[1]) == 0:
            raise Exception("invalid docker image name: %s" % docker_image)
        cmd = "docker images | egrep \"^%s \" | egrep \"%s\" | wc -l"%(
                img[0], img[1])
    else:
        cmd = "docker images | egrep \"^%s \" | " % docker_image
        cmd+= "egrep \"latest\" | wc -l"

    out = exec_cmd(cmd)
    if out.strip() == "0":
        linfo = "Downloading docker image: %s. " % docker_image
        linfo+= "This may take a few minutes..."
        logger.info(linfo,also_console = True)
        out = exec_cmd("docker pull %s" % docker_image)
    else:
        logger.debug("docker_image %s is present" % docker_image)


def container_exists(device_name):
    """ return true if a container (running or not running) with provided
        name already exists
    """ 
    cmd = "docker ps -aqf name=%s" % device_name
    return len(exec_cmd(cmd)) > 0

def container_is_running(device_name):
    """ return true if a container with provided name is currently running """

    cmd = "docker ps -qf name=%s" % device_name
    return len(exec_cmd(cmd)) > 0

def get_mgmtIP(device_name):
    cmd = """sudo docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'""" + " " + device_name.lower()
    mgmtip = exec_cmd(cmd)
    mgmtip = re.search("(\d+.\d+.\d+.\d+)",mgmtip).group(1)
    return mgmtip

def remove_flexswitch_container(device_name, device_pid=None, force=False):
    """ check if container exists.  If so, remove it else do nothing """
    
    if not force: force = container_exists(device_name)
    if force:
        logger.info("removing existing container %s" % device_name,also_console = True)
        # remove soft links for pid
        if device_pid is not None and \
            os.path.isfile("%s/%s" % (netns_dir, device_pid)):
            logger.debug("removing netns pid: %s" % device_pid)
            cmd = "rm %s/%s" % (netns_dir, device_pid)
            exec_cmd(cmd, ignore_exception=True)
        cmd = "docker rm -f %s" % device_name
        exec_cmd(cmd, ignore_exception=True)

def get_container_pid(device_name):
    """ based on container name, return corresponding docker pid """

    cmd = "docker inspect -f '{{.State.Pid}}' %s" % device_name
    pid = exec_cmd(cmd, ignore_exception=True)
    if pid is None:
        logger.error("failed to determine pid of %s, is it running?"%(
            device_name),also_console = True)
        return None
    return pid.strip()

def create_flexswitch_container(device_name, device_port, fs_image=None,
                                dopt=None):
    """ create flexswitch container with provided device_name. Calling
        function must call get_container_pid to reliably determine if 
        container was successfully started.
        Note, this function will first remove container if it currently exists
    """
    # remove container if currently exists
    remove_flexswitch_container(device_name)

    # kickoff requested container
    logger.info("creating container %s" % device_name,also_console = True)
    cmd = "docker run -dt --log-driver=syslog --privileged --cap-add ALL "
    if fs_image is not None:
        cmd+= "--volume %s:%s:ro " % (fs_image, gen_flex_path)
    if dopt is not None: cmd+= "%s " % dopt
    cmd+= "--hostname=%s --name %s -p %s:8080 %s" % (
        device_name, device_name, device_port, docker_image)
    out = exec_cmd(cmd, ignore_exception=True)
    if out is None:
        logger.error("failed to create docker container: %s, %s" % (
            device_name, device_port),also_console = True)
        return None
    return

def create_topology_connections(topo):
    """ try to create all required topology connections. This operation
        does not stop on failure, it will try to create all connections
        in provided topology dictionary
        returns boolean - all connections successful
    """
    # first cleanup any stale connections
    try: clear_stale_connections()
    except Exception as e: pass

    all_connections_success = True
    for device_name in topo:
        pid1 = topo[device_name]["pid"]
        if pid1=="" or pid1=="0":
            logger.debug("skipping connections for non-operational device: %s"%(
                device_name))
            continue
        for c in topo[device_name]["connections"]:
            try:
                if c["remote-device"] not in topo:
                    logger.error("failed to map %s" % c,also_console = True)
                    logger.debug("topology: %s" % pretty_print(topo))
                    all_connections_success = False
                    continue
                pid2 = topo[c["remote-device"]]["pid"]
                if pid2 == "" or pid2 =="0": continue
                if connection_exists(pid1, pid2, c["local-port"],
                    c["remote-port"]):
                    logger.debug("skipping existing connection %s:%s - %s:%s"%(
                        device_name, c["local-port"], 
                        topo[c["remote-device"]]["name"], c["remote-port"]))
                    continue
                logger.info("creating connection  %s:%s - %s:%s" % (
                    device_name, c["local-port"], 
                    topo[c["remote-device"]]["name"], c["remote-port"]),also_console = True)
                create_connection(pid1, pid2, c["local-port"],c["remote-port"])
            except Exception as e:
                logger.error("Error occurred: %s" % traceback.format_exc(),also_console = True)
                all_connections_success = False

        # rename management interface to ma1 now that netns has been setup
        # rename_mgmt(pid1)

    return all_connections_success

def connection_exists(pid1, pid2, link1, link2):
    """ returns True if connection already exists """

    link1_exists = False
    link2_exists = False
    out = exec_cmd("ip netns exec %s ip -o link" % pid1, ignore_exception=True)
    if out is not None:
        for l in out.split("\n"):
            r1 = re.search(link_state_reg, l.strip())
            if r1 is not None:
                if r1.group("intf") == link1: 
                    link1_exists = True
                    break
    out = exec_cmd("ip netns exec %s ip -o link" % pid2, ignore_exception=True)
    if out is not None:
        for l in out.split("\n"):
            r1 = re.search(link_state_reg, l.strip())
            if r1 is not None:
                if r1.group("intf") == link2: 
                    link2_exists = True
                    break
    return link1_exists and link2_exists
   
def create_connection(pid1, pid2, link1, link2):
    """ create connection between two docker containers """

    # verify pids and links
    if pid1 is None or pid2 is None or link1 is None or link2 is None or \
        len(pid1)==0 or len(pid2)==0 or len(link1)==0 or len(link2)==0:
        raise Exception("invalid connection arguments: %s, %s, %s, %s" % (
            pid1, pid2, link1, link2))

    # delete existing ethS/ethD in main namespace (ignore errors)
    exec_cmd("ip link delete ethS type veth", ignore_exception=True)
    exec_cmd("ip link delete ethD type veth", ignore_exception=True)

    # list of commands to execute
    cmds = ["mkdir -p %s" % netns_dir]

    # check if soft link exists, if not then create it
    if not os.path.isfile("%s/%s"%(netns_dir, pid1)):
        cmds.append("ln -s /proc/%s/ns/net %s/%s"%(
            pid1, netns_dir, pid1))
    if not os.path.isfile("%s/%s"%(netns_dir,pid2)):
        cmds.append("ln -s /proc/%s/ns/net %s/%s"%(
            pid2, netns_dir, pid2))

    # create connections
    cmds.append("ip link add ethS type veth peer name ethD")
    cmds.append("ip link set ethS netns %s" % pid1)
    cmds.append("ip link set ethD netns %s" % pid2)
    cmds.append("ip netns exec %s ip link set ethS name %s" % (pid1, link1))
    cmds.append("ip netns exec %s ip link set ethD name %s" % (pid2, link2))
    cmds.append("ip netns exec %s ip link set %s up" % (pid1, link1))
    cmds.append("ip netns exec %s ip link set %s up" % (pid2, link2))

    # execute commands
    for c in cmds: exec_cmd(c)

def clear_stale_connections():
    """ remove stale connection links in netns directory """
    logger.debug("cleaning up netns directory: %s" % netns_dir)
    for f in os.listdir(netns_dir):
        if not os.path.isfile("%s/%s" % (netns_dir, f)):
            logger.debug("removing stale softlink: %s/%s" % (netns_dir,f))
            os.remove("%s/%s" % (netns_dir, f))

def rename_mgmt(pid1, s="eth0", d="ma1"):
    """ rename default eth0 interface to ma1. Operation for docker mgmt
        interface needs to be shut, rename, no-shut
    """
    cmds = []
    cmds.append("ip netns exec %s ip link set %s down" % (pid1, s))
    cmds.append("ip netns exec %s ip link set %s name %s" % (pid1,s, d))
    cmds.append("ip netns exec %s ip link set %s up" % (pid1,d))
    
    # execute commands
    for c in cmds: exec_cmd(c, ignore_exception=True)

def cleanup(topo):
    """ cleanup topology by deleting containers and removing links """
   
    threads = []
    for device_name in sorted(topo.keys()):
        t = threading.Thread(target=remove_flexswitch_container,
                args=(device_name, topo[device_name]["pid"], True))
        threads.append(t)
    execute_threads(threads)

    try: clear_stale_connections()
    except Exception as e: pass


def verify_flexswitch_running(devices, timeout=90, uptime_threshold=10):
    """ for provided devices dictionary, wait for flexswitch to start
        if it has not started within the timeout manually start the process
    """
    logger.info("waiting for flexswitch to start...",also_console = True)
    device_state = {}
    for d in devices: 
        device_state[d] = {"name":d, "uptime":0, "ready":False,
            "port":devices[d]["port"]}
    start_ts = time.time()
    while start_ts + timeout > time.time():
        # loop through all devices and check if sysd is currently running
        waiting = False
        for d in device_state:
            cmd ="curl -s 'http://localhost:%s/public/v1/state/SystemStatus'"%(
                device_state[d]["port"])
            out = exec_cmd(cmd, ignore_exception=True)
            if out is not None:
                try:
                    js = json.loads(out)
                    if "Object" in js and "UpTime" in js["Object"] and \
                        "Ready" in js["Object"]:
                        uptime = js["Object"]["UpTime"]
                        ready = bool(js["Object"]["Ready"])
                        logger.debug("uptime for %s: %s, ready:%r" % (d, 
                            uptime, ready))
                        device_state[d]["uptime"] = uptime
                        # overwrite ready attribute if uptime is less than
                        # threshold
                        if "ms" in uptime: ready = False
                        elif "h" in uptime or "m" in uptime: pass
                        else:
                            ut = float(re.sub("s","", uptime))
                            if ut < uptime_threshold: ready = False
                        logger.debug("overwriting ready to: %r" % ready)
                        device_state[d]["ready"] = ready
                        if ready: continue
                               
                except ValueError as e:
                    logger.debug("failed to parse: %s" % e)
                    device_state[d]["ready"] = False
                    device_state[d]["uptime"] = 0
            # only if all conditions match do we skip reset of waiting flag
            waiting = True
        if waiting: time.sleep(1)
        else: break
    
    # check if any devices need to have flexswitch manually started
    manually_started = False
    for d in device_state:
        if not device_state[d]["ready"]:
            manually_started = True
            logger.info("timeout expired, restarting flexswitch on %s"%d,also_console = True)
            exec_cmd("docker exec -it %s service flexswitch start" % d)

    # best to go through process again to ensure service actually starts
    if manually_started:
        return verify_flexswitch_running(devices, timeout, uptime_threshold)
    # success
    logger.info("flexswitch is running on all containers",also_console = True)

def check_flexswitch_image(img=None):
    """ if image is a url, download the image and save to images/ cache 
        check that flexswitch image is formatted as docker deb package
            flexswitch_docker-(.*).deb
        return None if invalid else returns full image path
    """
    if img is None: return None
    img_reg = "^flexswitch_docker[a-z0-9\_\-\.]+\.deb$"
    # download image first if url is provided
    if re.search("^http", img) is not None:
        img_name = img.split("/")[-1]
        # validate img name (this will be repeated later again after download
        # but best if we skip the download if the image is not valid name)
        if not re.search(img_reg, img_name):
            logger.error("'%s' is not a valid flexswitch docker image"%img_name,also_console = True)
            return None
        # check if image is already available in fs_image_dir
        if not os.path.isfile("%s/%s" % (fs_image_dir, img_name)):
            logger.info("downloading image from %s" % img,also_console = True)
            ret = exec_cmd("wget -O %s/%s %s" % (fs_image_dir, img_name, img),
                ignore_exception=True)
            if ret is None:
                logger.error("failed to download image",also_console = True)
                try:
                    # wget -O creates file with zero size even on failed 
                    # download, need to delete it to prevent picking it up as 
                    # a cached copy
                    if os.path.isfile("%s/%s" % (fs_image_dir, img_name)):
                        logger.debug("deleting file: %s/%s" % (fs_image_dir, 
                            img_name))
                        os.remove("%s/%s" % (fs_image_dir, img_name))
                except IOError as e: pass
                return None
            # rename img to local file
            img = "%s/%s" % (fs_image_dir, img_name)

    # extract filename from path and ensure valid img name
    img_name = img.split("/")[-1]
    if not re.search(img_reg, img_name):
        logger.error("'%s' is not a valid flexswitch docker image" % img_name,also_console = True)
        return None
    if not os.path.isfile(img):
        # if file is not file, check the img_name against the cache directory
        # as last resort
        if not os.path.isfile("%s/%s" % (fs_image_dir, img_name)):
            logger.error("unable to access flexswitch image: %s" % img,also_console = True)
            return None
        else: img = "%s/%s" % (fs_image_dir, img_name)

    # verify size is not zero (1MB)
    if os.stat(img).st_size < 1024*1024*1:
        logger.error("invalid flexswitch image: %s, size: %s bytes"%(img_name, 
            os.stat(img).st_size),also_console = True)
        return None
    
    # everything looks ok, return full path
    return os.path.abspath(img)

def prompt_for_container_delete(topo):
    """ check if any container with device_name already exists, if so notify
        user that they will be deleted in order to continue with script.
        If user does not confirm, exit script
    """
    existing_containers = []
    for device_name in sorted(topo.keys()):
        if container_exists(device_name): 
            existing_containers.append(device_name)

    if len(existing_containers) > 0:
        print "\nThe following containers already exist:"
        for c in existing_containers: print "\t%s" % c
        msg = "You can see more details on each container by issuing "
        msg+= "'docker ps -a'"
        print msg
        choice = None
        prompt = """Press 1 to restart the existingcontainers.\nPress 2 to delete the existing containers.\nPress 3 to manually perform some operation."""
        try:
            while choice is None:
                choice = ("%s" % raw_input(prompt)).strip()
                if re.search("1", choice, re.IGNORECASE):
                    logger.info("Restarting the containers",also_console = True)
                    for c in existing_containers:
                        logger.info("Restarting %s container"%c,also_console = True)
                        exec_cmd("""docker exec %s sh -c "/etc/init.d/flexswitch restart" """ % c)
                    sys.exit("All Existing containers restarted")
                elif re.search("2", choice, re.IGNORECASE):
                    logger.info("Deleting the existing containers",also_console = True)
                elif re.search("3", choice,re.IGNORECASE):
                    msg = "\nCannot continue while current containers exists.\n"
                    msg+= "Please manually delete appropriate containers and then "
                    msg+= "rerun this script\n"
                    sys.exit(msg)
                else:
                    print "Please press 1 or 2"
                    choice = None
        except KeyboardInterrupt as e: sys.exit("\nExiting...\n")
       
            

def execute_threads(threads):
    """ receive list of threading.Thread objects that have not yet been 
        started. Start each thread and Ensure that only MAX_THREADS are 
        running at a time. Ensure all threads complete
    """
    batch_count = 0
    logger.debug("execute %s threads batch-size:%s"%(len(threads),MAX_THREADS))
    while len(threads)>0:
        batch_count+=1
        active_threads = []
        while len(threads)>0 and len(active_threads) < MAX_THREADS:
            active_threads.append(threads.pop())
        # start batch of threads
        logger.debug("starting batch:%s" % batch_count)
        for t in active_threads:
            t.setDaemon(True)
            t.start()
            time.sleep(0.1)
        # wait until all threads end
        for t in active_threads: t.join()
        logger.debug("completed batch:%s (%s remaining)" % (batch_count, 
            len(threads)))

def updateTestBed(testBed_file):
    with open(testBed_file, "r") as f: js = json.load(f)
    dev_List = sorted(js["Device"].keys())
    for device in dev_List:
        mgmtip = get_mgmtIP(device)
        print mgmtip
        js[Device][device][mgmtIP] = mgmtip
    with open(testBed_file, "w") as f: 
        json.dump(js,f,indent = 4,sort_keys = True)
    print (pretty_print(js))
    return
      
 
   
if __name__ == "__main__":

    try:
        # ensure script working directory is local directory
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
 
        # verify we're running on Linux box
        out = exec_cmd("uname", ignore_exception=True)
        if out is None or "linux" not in out.lower():
            rmsg = "The underlying operating system is not Linux. "
            rmsg+= "Docker with flexswitch is not supported"
            sys.exit(rmsg)
    
        # get user arguments
        #args = get_args()
        #testBed_path = args.testBedPath
        print testBed_path
        
        # verify user is running as root before preceeding further
        if os.geteuid() != 0:
            rmsg = "Sorry, you must be root. "
            rmsg+= "Use 'sudo python %s' to execute this script." % __file__
            sys.exit(rmsg)
    
        # check that docker is running
        if not check_docker_running():
            emsg = "Cannot connect to Docker daemon.  Is it running?\n"
            emsg+= "Try 'sudo service docker start' to enable the service"
            sys.exit(emsg)
    
        # build/validate topology file from provided lab
        topo = get_topology("%s" %testBed_path)
        if topo is None:
            logger.error("failed to parse device topology",also_console = True)
            sys.exit(1)
 
        # prepare for creating new containers...
        # any containers that will be automatically deleted
        prompt_for_container_delete(topo)
    
        # check if flexswitch is present, if not perform docker pull
        try: check_docker_image()
        except Exception as e:
            logger.error("Failed to verify/pull docker image: %s" % e,also_console = True)
            sys.exit(1)
    
        # create containers and map pid to each device in topology
        start_success = True
        threads = []
        for device_name in sorted(topo.keys()):
            t = threading.Thread(target=create_flexswitch_container,
                args=(device_name, topo[device_name]["port"], None,
                None))
            threads.append(t)
        execute_threads(threads)

        # gather pid for each device
        for device_name in topo:
            pid = get_container_pid(device_name)
            if pid is None: 
                logger.error("'%s' failed to start" % device_name,also_console = True)
                start_success = False
                break
            topo[device_name]["pid"] = pid
    
        # create topology connections
        if start_success:
            start_success = create_topology_connections(topo)
    
        if start_success:
            # verify/wait for flexswitch to start on all containers
            verify_flexswitch_running(topo)
            # apply stage configs
            #if args.stage>0: execute_stages(current_lab["path"], args.stage)
            #logger.info("Successfully started '%s'" % current_lab["name"])
            print "done"
        else:
            logger.error("failed to build topology, cleaning up...",also_console = True)
            cleanup(topo)

        updateTestBed("%s" %testBed_path)
       


    except KeyboardInterrupt as e: 
        sys.exit("\nExiting...\n")
    

"""
def get_args():
    try:
        desc = "Docker Tool"
        print "In args"
        parser = argparse.ArgumentParser(description=desc,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        print "args1"
        parser.add_argument("--testBedPath", action="store_true", dest="testBedPath",
             help="Specifies the TestBed Path")
        print "args2"
        # parse arguments
        args = parser.parse_args()
        print args
        return args
    except Exception as ex:
	print type(ex)
"""

