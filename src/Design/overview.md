# main
preset variables
load config
load libraries
parse command line

validate usage: <app> {c/s/e}
output loaded settings
prompt to continue or quit

// need to launch server then emulator then client
//  ... can add functionality to check for presence

if 'c' then run client (manual mode)
if 's' then run server
if 'e' then run emulator
if 'h' then display instructions
if 'l' then list configuration details
[if 'd' then run demo (auto mode)]
else error out with information

# server (aka slave)
load file structure
open socket to listen
if a message arrives then acknowledge and parse it
open reverse socket to client

if command is to get then run send (file name)
if command is to put then run recv (file name)
if command is catalog then run catalog

close socket
return to beginning

# client (aka master)
load file structure
open socket to emulator [or server/slave]

wait for user input
validate user input

open
if get then call get
if send the call send
if catalog then call catalog

[# demo / auto mode
// needs file structure handle, primary socket handle, secondary socket handle

call get listing
for each file name
    call send file name

open file structure
for each file
end demo/auto mode]

# emulator
If error rate not on command line
    if error rate not in config file
		ask client for error rate
Set lost packet sequence number (function)

open socket to server
open socket to client
[
    open reverse socket to server on client
    open reverse socket to client on server
]

listen on server socket, 
listen on return socket from client
[
    listen on reverse server socket from client, 
    listen on reverse return socket from server
]

for each packet received
    if first packet 
        save socket info
        include 'corrected' destination for messages 
        based on socket and source IP

    if was-packet-lost()
        add drop packet flag to message
    else
        send packet on to destination
    save pktinfo to log file
    
# send
open file to send
while !EOF
    packetize data
    while next slot is open
        add packet to slot
    for i=1 to window_size
        send packet
        set timeout = now+delay
        intransit++ / sent ++
    if ack received
        for (oldest packet) to (ack received)
            mark packet ackd
            intransit -- / tail++
    if oldest_packet timeout
        resend packet
        reset timeout
    if slot >= window_size
        slot=0
close file

# receive
open file to receive
while !EOF
    listen on socket
    put message into queue
    if next in sequence
        send ack
        seq++
    if next packet is in queue
        depacketize to file
        clear from queue
close file

# catalogue (file structure handle, socket handle)
packetize and send files listing

# set lost packet sequence number
Lost packet is random*err-rate
(where 1 in x is the error rate, x = err-rate)

# was-pkt-lost
If sequence == lost-packet
	Lost = true
Else 
	lost=false

If sequence++ == err-rate
	sequence=0
	Update lost packet sequence number
