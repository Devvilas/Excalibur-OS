from os import system
import os as os
from time import sleep
from installer import BOOT_MODE
from installer import layout
from installer import disk_to_parted

system("arch-chroot /mnt")

system("cd")

system("ls /usr/share/zoneinfo/** | less")

time_zone = input("Write your time zone ex: Europe/Lisbon\nTime zone> ")

system("ln -sf /usr/share/zoneinfo/" + time_zone + " /etc/localtime")

system("hwclock --systohc")

print("Please see name of the language in UTF-8 (recommended) and write it then...")
input("Press enter to continue")

system("cat /etc/locale.gen | less")

lang = input("ex: pt_PT.UTF-8\nLang> ")

system("rm -r /etc/locale.gen")

system("touch /etc/locale.gen")

system("echo " + lang + " > /etc/locale.gen")
system("touch /etc/locale.conf")
system("""echo "LANG=""" + lang + """" > /etc/locale.conf""")

system("locale-gen")

system("touch /etc/vconsole.conf")
system("echo KEYMAP=" + layout + " > /etc/vconsole.conf")


system("clear")

print("Ok! Now let me ask something...\nWhat will be the name of your linux machine?")
hostname = input("hostname> ")

system("touch /etc/hostname")
system("echo " + hostname + " > /etc/hostname")

system("clear")

print("Now to the ROOT USER (dangerous), you need to setup the password...")

system("passwd")

system("clear")

print("Lets install the GRUB bootloader!")
input("Press enter to start GRUB installation")
if BOOT_MODE == "efi":
    system("pacman -S grub efibootmgr")
    system("grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB_EXCAL --recheck")
if BOOT_MODE == "bios":
    system("pacman -S grub")
    system("grub-install --target=i386-pc /dev/sd" + disk_to_parted)

system("echo GRUB_DISABLE_OS_PROBER=false > /etc/default/grub")
system("grub-mkconfig -o /boot/grub/grub.cfg")

system("clear")

print("Now you only use ROOT and... its kinda of danger...\nSo... LETS CREATE A USER! (with sudo, yes...)")


system("pacman -S dosfstools os-prober mtools network-manager-applet networkmanager wpa_supplicant wireless_tools dialog sudo nano xorg xorg-server")
system("systemctl enable NetworkManager")
system("pacman -S firefox neofetch")
system("echo neofetch >> /etc/bash.bashrc")

name = input("Name> ")
system("useradd -m -g users -G wheel sudo " + name)

system("passwd " + name)

system("echo blacklist pcspkr > /etc/modprobe.d/nobeep.conf")

print("Installer not done\nVERSION: DEVELOPING... \nSYSTEM CODE NAME: EXCAL")

system("exit && umount -R /mnt && reboot")