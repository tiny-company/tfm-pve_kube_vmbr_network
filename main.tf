
# ------------------------------------------------------------------
# - Filename: main.tf
# - Author : draed
# - Dependency : none
# - Description : terraform module that create a kubernetes network on pve
# - Creation date : 2025-02-17
# - terraform version : OpenTofu v1.9.0
# ------------------------------------------------------------------

resource "null_resource" "import_script_dependencies" {
  provisioner "local-exec" {
    command = "virtualenv -p ${var.python_version} ${path.module}/venv && . ${path.module}/venv/bin/activate && pip install -r ${path.module}/scripts/requirements.txt"
  }
  lifecycle {
    ignore_changes = all
  }
}

resource "null_resource" "get_highest_vmbr_id" {
  provisioner "local-exec" {
    command = "${path.module}/venv/bin/python ${path.module}/scripts/get_highest_vmbr_id.py > ${path.root}/highest_vmbr_id.txt"
    environment = {
      PROXMOX_API_HOST = "${var.proxmox_api_host}"
      PROXMOX_API_NODENAME = "${var.proxmox_api_nodename}"
      PROXMOX_API_USERNAME = "${var.proxmox_api_username}"
      PROXMOX_API_TOKENNAME = "${var.proxmox_api_tokenname}"
      PROXMOX_API_TOKENVALUE = "${var.proxmox_api_tokenvalue}"
    }
  }
  lifecycle {
    ignore_changes = all
  }
  depends_on = [null_resource.import_script_dependencies]
}

data "local_file" "highest_vmbr_id" {
  filename = "${path.root}/highest_vmbr_id.txt"
  depends_on = [null_resource.get_highest_vmbr_id]
}

## delete venv folder (keep env clean)
resource "null_resource" "delete_file" {
  provisioner "local-exec" {
    command = "rm -rf ${path.module}/venv"
  }
  depends_on = [null_resource.import_script_dependencies, null_resource.get_highest_vmbr_id]
}

## create kubernetes network 
## see doc at : https://search.opentofu.org/provider/bpg/proxmox/latest/docs/resources/virtual_environment_network_linux_bridge 
resource "proxmox_virtual_environment_network_linux_bridge" "vmbr_internal_net" {
  node_name = var.proxmox_api_nodename
  name      = trimspace(data.local_file.highest_vmbr_id.content)
  comment = var.proxmox_network_comment
}