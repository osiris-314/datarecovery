#!/usr/bin/env python3
import subprocess
from colorama import Fore, Style

def list_disks():
    # Run the lsblk command and capture its output
    result = subprocess.run(['lsblk', '-o', 'NAME,RM,TYPE,SIZE'], stdout=subprocess.PIPE, text=True)
    
    # Split the output into lines
    lines = result.stdout.strip().split('\n')
    
    # Extract the headers and the disk information
    headers = lines[0].split()
    disks_info = lines[1:]
    
    # Create a list to store the disk information
    disks = []

    # Iterate over the disk information
    for disk in disks_info:
        # Split each line by spaces
        disk_data = disk.split()
        name = disk_data[0]
        removable = disk_data[1]
        dtype = disk_data[2]
        size = disk_data[3]
        
        # Filter out partitions and only get the base disk names
        if dtype == 'disk':
            is_removable = "Yes" if removable == '1' else "No"
            disk_info = (name, size, is_removable)
            disks.append(disk_info)
    
    return disks

def format_table(disks, title):
    table = f"{title}"
    table += f"{'Disk':<10}{'Size':<10}{'Removable':<10}\n"
    table += "-"*30 + "\n"
    for disk in disks:
        name, size, is_removable = disk
        table += f"{name:<10}{size:<10}{is_removable:<10}\n"
    return table

def recover_data():
    disks = list_disks()
    table = format_table(disks, '')
    print(table)
    disk_choice = input('Enter the name of the disk to recover data from (e.g., sda): ')
    print(Fore.LIGHTBLUE_EX + 'Recovering deleted data from the disk...\n' + Fore.LIGHTGREEN_EX)
    subprocess.run(f'sudo foremost -T -Q -i /dev/{disk_choice}', shell=True)

def main():
    recover_data()

if __name__ == '__main__':
    print('\n')
    main()
