#!/bin/sh
clear while : do
  exec ./force_install_dir/RustDedicated -batchmode -nographics
  -server.ip 91.121.88.22
  -server.port 28015
  -rcon.ip 91.121.88.22
  -rcon.port 28016
  -rcon.password "abcde"
  -server.maxplayers 75
  -server.hostname "Nomca"
  -server.identity "my_server_identity"
  -server.level "Procedural Map"
  -server.seed 12345
  -server.worldsize 3000
  -server.saveinterval 300 -server.globalchat true
  -server.description "Description Here"
  -server.headerimage "http://static4.businessinsider.com/image/56cba4ed6e97c629008b8dca-1190-625/donald-trumps-favorite-excuse-it-was-just-a-retweet.jpg"
  -server.url "boyodarwin.me"
  echo "nRestarting server...n" done