#!/bin/bash
#since google ended TTS, this wrapper-script replaces tts with pico2wave.
#version 0.2 -now rudimentarily handles language -l param.

if [ $# -lt 1 ]  
then                  #no argument entered - i need something to say
   /usr/bin/pico2wave -w /tmp/tempsound.wav "I have nothing to say." 
   /usr/bin/aplay -q /tmp/tempsound.wav
   rm /tmp/tempsound.wav
   exit 0
fi

if [ "$1" = "-l" ]    #-l in event where user explicitly defines language.  
then                   # Note: always assumes $2 is 'en' or a valid language option. 
   lang=$2
   if [ $lang = "en" ]   #TODO: cant find the real source of en, but if 
   then                      # i see 'en' I'm hard coding  en-US.
      lang="en-US"       #US English, mofo, do you speak it  
   fi           
   shift 2  
   speech=$@  
   /usr/bin/pico2wave -l $lang -w /tmp/tempsound.wav "$speech" 
   /usr/bin/aplay -q /tmp/tempsound.wav
   rm /tmp/tempsound.wav
   exit 0
else                  #else lets go straight to speech-output
  speech=$@  
  /usr/bin/pico2wave -w /tmp/tempsound.wav "$speech"  
  /usr/bin/aplay -q /tmp/tempsound.wav
  rm /tmp/tempsound.wav
fi 