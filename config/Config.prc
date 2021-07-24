# This is the PRC configuration file for public releases of the game.
# It's rather similar to the dev PRC, but w/ some unneeded options removed.

# VFS for resources.
model-path resources
model-cache-models #t
model-cache-textures #t
vfs-mount resources/phase_3 /phase_3
vfs-mount resources/phase_3.5 /phase_3.5
vfs-mount resources/phase_4 /phase_4
vfs-mount resources/phase_5 /phase_5
vfs-mount resources/phase_5.5 /phase_5.5
vfs-mount resources/phase_6 /phase_6
vfs-mount resources/phase_7 /phase_7
vfs-mount resources/phase_8 /phase_8
vfs-mount resources/phase_9 /phase_9
vfs-mount resources/phase_10 /phase_10
vfs-mount resources/phase_11 /phase_11
vfs-mount resources/phase_12 /phase_12
vfs-mount resources/phase_13 /phase_13
default-model-extension .bam

# Client settings
window-title Toontown Offline
server-version ttoff
build-version 2.5.0
sync-video #f
want-dev #f
preload-avatars #t
texture-anisotropic-degree 16
icon-filename phase_3/etc/icon.ico
audio-library-name p3fmod_audio
default-directnotify-level info
smooth-lag 0.4
# Pretty sure you're gonna want membership...
want-membership #t


# Fix for newer Nvidia GPU's to lower the gamma
load-display pandagl
color-bits 8 8 8
alpha-bits 8


# DC Files
dc-file config/ttoff.dc


# Game Features
want-estates #t
# They work fine.
want-clarabelle-voice #t
# Enables Clarabelle's voice from TTR.
want-pets #t
# They seem to work fine.
want-news-tab #f
want-news-page #f
# These work fine, but I dont know if they would be very useful
want-accessories #t
# Occasional AI Crash
want-parties #t
# Kinda unfinished.
want-gardening #f
# Not implemented.
want-gifting #f
# Not needed.
want-cogdominiums #t
# These also work!
want-boarding-groups #t
# Works. Of course, offline won't need these.
want-cheesy-expirations #f
# Don't set this to true, then cheesy effects are lost upon reboot :(
want-toontorial #t
# Leave this on true, as you can just skip on Make-A-Toon anyways. Works perfect.
want-code-redemption #t
# Works great!
want-new-toonhall #t
# Toon Hall w/ Silly Meter.
want-skip-button #t
# Skip button that TTR disabled by default.
want-fnaf #t
# Five Nights at the Factory by Toontown House, developed by Loblao.
want-picnic-games #f
# Picnic table games. They work but the placement is broken for the tables.

# Playgrounds
want-playgrounds #t
want-toontown-central #t
want-donalds-dock #t
want-daisy-gardens #t
want-minnies-melodyland #t
want-the-brrrgh #t
want-donalds-dreamland #t
want-goofy-speedway #t
want-acorn-acres #t
want-minigolf #t
want-toonfest #t

# Cog HQs
want-cog-headquarters #t
want-sellbot-hq #t
want-cashbot-hq #t
want-lawbot-hq #t
want-bossbot-hq #t

# Classic Characters
want-classic-chars #t
want-mickey #t
want-donald-dock #t
want-daisy #t
want-minnie #t
want-pluto #t
want-donald-dreamland #t
want-goofy #t
want-chip-and-dale #t

# Misc. Modifications
estate-day-night #t
want-instant-parties #t
show-total-population #f

# Chat Features-- These should remain untouched. As this is an offline game, we do not need a whitelist.
want-whitelist #f
force-avatar-understandable #t
force-player-understandable #t

# Makeshift Holiday Manager
force-holiday-decorations 6
want-arg-manager #f
want-mega-invasions #f
mega-invasion-cog-type tm
