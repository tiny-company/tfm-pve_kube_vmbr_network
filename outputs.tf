output "lxc_highest_id_value" {
  description = "highest existing vmbr network id +1 on proxmox node"
  value = trimspace(data.local_file.highest_vmbr_id.content)
}
