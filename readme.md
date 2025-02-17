# tfm-pve_kube_network

## Description

A simple terraform module that create a kubernetes vmbr network in proxmox provider.

## prerequisite

- None

## Usage 

- Import the module by referencing it in your main terraform file (`main.tf`) using :
```hcl
## Create Kubernetes nodes ressource
module "proxmox-kube_node" {
  source = "git::https://github.com/tiny-company/tfm-pve_kube_nodes"
  kube_node_description = var.kube_node_description
  terraform_proxmox_node_name = var.terraform_proxmox_node_name
  terraform_proxmox_lxc_highest_id_value = module.proxmox-kube_master.kube_master_highest_vmid
  kube_node_cpu_arch = var.kube_node_cpu_arch
  kube_node_cpu_cores = var.kube_node_cpu_cores
  kube_node_disk_datastore = var.kube_node_disk_datastore
  kube_node_disk_size = var.kube_node_disk_size
  kube_node_mem_dedi = var.kube_node_mem_dedi
  kube_node_mem_swap = var.kube_node_mem_swap
  kube_node_os_templ_file = var.kube_node_os_templ_file
  kube_node_os_type = var.kube_node_os_type
  kube_node_hostname = var.kube_node_hostname
  kube_node_ipv4_start_addr = var.kube_node_ipv4_start_addr
  kube_node_ipv4_mask = var.kube_node_ipv4_mask
  kube_node_ipv4_gw = var.kube_node_ipv4_gw
  kube_node_ssh_pub_keys = var.default_root_ssh_pub_keys
  kube_node_net_int_name = var.kube_node_net_int_name
}
```

- Don't forget to define the vars below in your main variables.tf :
```hcl
variable "python_version" {
  type      = string
  default   = "3.11.2"
}

variable "proxmox_api_host" {
  type      = string
  sensitive = true
}

variable "proxmox_api_nodename" {
  type      = string
  sensitive = true
}

variable "proxmox_api_username" {
  type      = string
  sensitive = true
}

variable "proxmox_api_tokenname" {
  type      = string
  sensitive = true
}

variable "proxmox_api_tokenvalue" {
  type      = string
  sensitive = true
}

variable "proxmox_network_comment" {
  type      = string
  sensitive = true
}
```

- And finally don't forget to set **these vars** and **the vars for the proxmox/bpg provider** in a .tfvars (i.e: `terraform.tfvars`) file  :
```hcl
pve_endpoint="https://proxmox_endpoint_url/"
pve_token="proxmox_username@authentication_base!token_name=0000000-00000-00000-000000-4532433"
proxmox_api_host="proxmox_endpoint"
proxmox_api_tokenname="token_name"
proxmox_api_tokenvalue="0000000-00000-00000-000000-4532433"
proxmox_api_username="proxmox_username@authentication_base"
proxmox_network_comment="a new proxmox vmbr network"
```

## Sources : 

- [tutorial terraform module](https://developer.hashicorp.com/terraform/tutorials/modules/module)
- [terraform module creation guide](https://developer.hashicorp.com/terraform/language/modules/develop)
- [terraform module source](https://developer.hashicorp.com/terraform/language/modules/sources#github)
- [terraform module git private repo source](https://medium.com/@dipandergoyal/terraform-using-private-git-repo-as-module-source-d20d8cec7c5)