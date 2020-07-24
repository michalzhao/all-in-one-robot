# All-in-one-robot
The idea is to build a robot which can see, listen, sense and can be controlled via voice etc.

# setup Email send server:
sudo nano /etc/ssmtp/ssmtp.conf

It needs to include this:
root=postmaster
mailhub=smtp.gmail.com:587
hostname=raspberrypi
AuthUser=AGmailUserName@gmail.com
AuthPass=TheGmailPassword
FromLineOverride=YES
UseSTARTTLS=YES

# motion config
sudo nano /etc/motion/motion.conf

# Startup script
sudo nano /etc/rc.local

# services on system start
/etc/init.d/

