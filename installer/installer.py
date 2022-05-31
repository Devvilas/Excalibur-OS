from os import system
import os as os
from time import sleep



print("Welcome")
sleep(1)
print("Welcome to the Excalibur Installer!\nI will help you installing your new system!")

sleep(2)

print("First step!")
sleep(1)
print("I will display the all layouts avaible then press Q to leave and write the layout that you choosed PS: The layout that you choose here, will be the same for the new system...")

input("Press enter to display layouts")

system("ls /usr/share/kbd/keymaps/**/*.map.gz | less")

layout = input("Choose your layout: ")

system("loadkeys " + layout)

if os.path.exists("/sys/firmware/efi/efivars"):
    BOOT_MODE = "efi"
if not os.path.exists("/sys/firmware/efi/efivars"):
    BOOT_MODE = "bios"


system("clear")

print("Activating system clock...")
system("timedatectl set-ntp true")


system("clear")

print("Now its time to setup the local where will live your system")
input("Press enter to enter in the edit partition mode")

system("clear")

system("fdisk -l")

print("Write the last letter of the disk you choosed, ex: /dev/sda ---> a")

disk_to_parted = input("choose_disk> ")

system("fdisk /dev/sd" + disk_to_parted)

system("clear")
print("Now you need to specif the numbers of the partitions that you created")

ROOT_PART = input("Number_ROOT> ")
SWAP_PART = input("Number_SWAP> ")
if BOOT_MODE == "efi": 
    EFI_PART = input("Number_EFI> ")
if BOOT_MODE == "bios":
    pass

if BOOT_MODE == "efi":
    print("Formating EFI Partition...")
    system("mkfs.fat -F 32 /dev/sd" + disk_to_parted + EFI_PART)

print("Formating ROOT Partition...")
system("mkfs.ext4 /dev/sd" + disk_to_parted + ROOT_PART)

print("Formating SWAP Partition...")
system("mkswap /dev/sd" + disk_to_parted + SWAP_PART)

print("mounting...")

system("mount /dev/sd" + disk_to_parted + ROOT_PART + " /mnt")
system("mkdir -p /mnt/boot")
system("mount /dev/sd" + disk_to_parted + EFI_PART + " /mnt/boot")

system("swapon /dev/sd" + disk_to_parted + SWAP_PART)

print("Mounted")

system("clear")

print("Lets download now the system!")

input("Press enter to download base system")

system("time pacstrap /mnt base linux linux-firmware")


system("genfstab -U /mnt >> /mnt/etc/fstab")

system("clear")

print("Now, your system is installed but is not with the Excalibur scripts and other things...")

print("Execute python3 chroot.py")