# tfm-pve_kube_network

## Description

A simple terraform module that create a kubernetes vmbr network in proxmox provider by getting automatically the highest vmbr network value from proxmox node.

## prerequisite

- None

## Usage 

- Import the module by referencing it in your main terraform file (`main.tf`) using :
```hcl
## Create Kubernetes nodes ressource
module "proxmox-kube_vmbr_network" {
  source = "git::https://github.com/tiny-company/tfm-pve_kube_vmbr_network"
  proxmox_api_host = var.proxmox_api_host
  proxmox_api_nodename = var.terraform_proxmox_node_name
  proxmox_api_username = var.proxmox_api_username
  proxmox_api_tokenname = var.proxmox_api_tokenname
  proxmox_api_tokenvalue = var.proxmox_api_tokenvalue
  proxmox_network_comment = var.proxmox_network_comment
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