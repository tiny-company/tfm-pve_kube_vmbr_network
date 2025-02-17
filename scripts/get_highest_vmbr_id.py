import requests
import os

from dotenv import load_dotenv
from proxmoxer import ProxmoxAPI


def instanciate_proxmox(PROXMOX_API_HOST: str, PROXMOX_API_USERNAME: str, PROXMOX_API_TOKENNAME: str, PROXMOX_API_TOKENVALUE: str) -> ProxmoxAPI:
    """
    instanciate proxmox using given parameters loaded from env var

    Parameters:
    - PROXMOX_API_HOST : proxmox host address
    - PROXMOX_API_USERNAME : proxmox username used to connect to pve
    - PROXMOX_API_TOKENNAME : proxmox token name used to connect to pve
    - PROXMOX_API_TOKENVALUE : proxmox token value used to connect to pve

    Returns:
    proxmox: instance of ProxmoxAPI 

    Raises:
    ValueError: If ProxmoxAPI instanciation failed
    """
    try:
      proxmox = ProxmoxAPI(
        PROXMOX_API_HOST, user=PROXMOX_API_USERNAME, token_name=PROXMOX_API_TOKENNAME, token_value=PROXMOX_API_TOKENVALUE, verify_ssl=False
      )
      return proxmox
    except ValueError as e:
      print(f"Error: {e}")
    
def get_highest_vmbr(proxmox, nodename: str) -> str:
    """
    get the highest vmbr network on a proxmox for a nodes and return highest +1

    Parameters:
    - proxmox : instance of ProxmoxAPI
    - nodename: proxmox node name

    Returns:
    highest_vmbr: highest existing vmbr network name +1 as string 

    Raises:
    ValueError: If request to proxmox failed
    """
    try:
      networks = proxmox.nodes(nodename).network.get()
      ## filter to get only bond network
      networks = proxmox.nodes(PROXMOX_API_NODENAME).network.get()
      bridge_network = list(filter(lambda item: item['type'] == 'bridge', networks))
      final_bridge_network = list(network['iface'] for network in bridge_network)
      ## get the highest network value assuming the highest vmbr is determined by the name (e.g., vmbr0, vmbr1, ...)
      highest_vmbr = None
      highest_index = -1
      for network_name in final_bridge_network:
          index = int(network_name.replace('vmbr', ''))
          if index > highest_index:
              highest_index = index
              highest_vmbr = network_name
      ## add 1 to generate next vmbr_id to use
      highest_vmbr = 'vmbr' + str(int(highest_vmbr.replace('vmbr', '')) +1)
      return highest_vmbr
    except ValueError as e:
      print(f"Error: {e}")

if __name__ == "__main__":

  ## load parameters from env var
  load_dotenv()
  PROXMOX_API_HOST = os.getenv('PROXMOX_API_HOST')
  PROXMOX_API_NODENAME = os.getenv('PROXMOX_API_NODENAME')
  PROXMOX_API_USERNAME = os.getenv('PROXMOX_API_USERNAME')
  PROXMOX_API_TOKENNAME = os.getenv('PROXMOX_API_TOKENNAME')
  PROXMOX_API_TOKENVALUE = os.getenv('PROXMOX_API_TOKENVALUE')

  ## instanciate proxmox conn
  proxmox = instanciate_proxmox(PROXMOX_API_HOST, PROXMOX_API_USERNAME, PROXMOX_API_TOKENNAME, PROXMOX_API_TOKENVALUE)
  
  ## get the highest lxc container id
  highest_vmbr = get_highest_vmbr(proxmox, PROXMOX_API_NODENAME)
  print(highest_vmbr)
