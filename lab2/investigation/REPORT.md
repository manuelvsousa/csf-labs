First we analyse the partition table on the disk:

```sh
# mmls -r sally_disk
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0019922943   0019920896   Linux (0x83)
003:  -------   0019922944   0019924991   0000002048   Unallocated
004:  Meta      0019924990   0020969471   0001044482   DOS Extended (0x05)
005:  Meta      0019924990   0019924990   0000000001   Extended Table (#1)
006:  001:000   0019924992   0020969471   0001044480   Linux Swap / Solaris x86 (0x82)
007:  -------   0020969472   0020971519   0000002048   Unallocated
```

```sh
# mmls -r -a sally_disk
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
002:  000:000   0000002048   0019922943   0019920896   Linux (0x83)
006:  001:000   0019924992   0020969471   0001044480   Linux Swap / Solaris x86 (0x82)
```

This means there are two partitions, 002 and 006. We extracted them to 002.dd and 006.dd, using dd:
```sh
# dd if=sally_disk bs=512 skip=2048 count=19920896 of=002.dd
19920896+0 records in
19920896+0 records out
10199498752 bytes (10 GB, 9.5 GiB) copied, 342.447 s, 29.8 MB/s
dd if=sally_disk bs=512 skip=2048 count=19920896 of=002.dd  6.76s user 42.47s system 14% cpu 5:42.45 total

# dd if=sally_disk bs=512 skip=19924992 count=1044480 of=006.dd
1044480+0 records in
1044480+0 records out
534773760 bytes (535 MB, 510 MiB) copied, 6.60595 s, 81.0 MB/s

```

Partition 006.dd is a linux swap partition, it might have important RAM cache information. We hope it doesn't use any compression method like zcache.
Partition 002.dd contains a linux ext4 filesystem:

```sh
# file 002.dd 
002.dd: Linux rev 1.0 ext4 filesystem data, UUID=d4a07e91-7492-4452-b318-8ec8ec4cb46b (extents) (large files) (huge files)
# file 006.dd 
006.dd: Linux/i386 swap file (new style), version 1 (4K pages), size 130559 pages, no label, UUID=0e048a98-5e7d-4d76-a27d-ae75a92b558a
```

```sh
# sudo mkdir /var/run/forimage
# sudo mount -t ext4 -o loop ./002.dd /var/run/mount/forimage
```

Then we enter a chroot environment:
```sh
# sudo chroot /run/mount/forimage /bin/bash
# PATH=/bin:/usr/bin
```

The we list all the users:
```sh
/# cut -d: -f1 /etc/passwd
root
daemon
bin
sys
sync
games
man
lp
mail
news
uucp
proxy
www-data
backup
list
irc
gnats
nobody
systemd-timesync
systemd-network
systemd-resolve
systemd-bus-proxy
syslog
_apt
messagebus
uuidd
lightdm
whoopsie
avahi-autoipd
avahi
dnsmasq
colord
speech-dispatcher
hplip
kernoops
pulse
rtkit
saned
usbmux
sally
```


We also listed the commands present on .bash_history:
```sh
/home/sally# cat .bash_history 
cd ~/Downloads/LiME/src/
sudo insmod lime-4.15.0-38-generic.ko "path=/tmp/sally_mem format=lime"
scp /tmp/sally_mem dmbb@turbina.gsd.inesc-id.pt:/home/dmbb/sally_mem_12
```

We then proceeded to evalutate memory, as we didn't found anythign interesting yet on the filesystem. We began by setting up volatolity to use our memory image:
```sh
export VOLATILITY_PROFILE=LinuxUbuntu160405x64
export VOLATILITY_LOCATION=/home/xtrm0/x/school/CSF/lab2/artifacts/sally_mem
```
And then we ran a volatility shell
```
volatility volshell
```

# Questions Investigation

Check Processes and their start date (use this to find out suspicious processes):

```
vol.py --profile=LinuxUbuntu160405x64 -f sally_mem linux_pslist
```

Then we ran volatility in order to get the proc maps for our process.

```
vol.py --profile=LinuxUbuntu160405x64 -f sally_mem linux_proc_maps -p 14921
```
We only dumped memory related to the identified process to a forder by doing:

```
vol.py --profile=LinuxUbuntu160405x64 -f sally_mem linux_proc_maps -p 14921 --dump-dir dump/
```

This file:
```
task.14921.0x7f127fbf4000.vma.strings
```

Contains stuff related to the encription key that was used in AES Counter mode.
```
echo "47683b9a9663c065353437b35c5d8519" > key.txt
```

We found this echo being made. We believe this is the key as this is a string with 32 characters represented in hexadecimal meaning that each characters represents 1 Byte, so 16 bytes in total. As the lab specification tells us that the key has 128 bits, this might be correct.


This file also contains information about a ssh connection that was made and shows a username and hostname of a possible ssh connection
```
jason@optiplex
```

This file contains more information about a possible ssh connection made by the malware.
```
task.14921.0x7f127fbf4000.vma.strings
```

