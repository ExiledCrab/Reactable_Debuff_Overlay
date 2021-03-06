# ExiledCrab's Reactable Debuff Overlay for PoE
Reactable Debuff Overlay is a tool to help people (like me) who already had a ton of trouble taking care of debuffs in Path of Exile. With the new nerfs to flasks, piano-flasking to keep up immunity is gone.

GGG stated that they wanted debuffs and flasks to be a 'reaction' mechanic, and not a spam mechanic. This is totally fine until you realize that some people have trouble figuring out which specfic debuff they have in a reasonable amount of time due to UI clutter and no customization.

If that sounds like you, then this tool is for you!

## IMPORTANT THINGS
1. This is a tool to package information already available in the UI into an easier to digest format
2. This tool lets you play PoE the way GGG says they want you to without any headaches
3. This tool will NEVER ALLOW ANY TYPE OF AUTOMATION OF GAME MECHANICS
4. This tool will NEVER PLAY ANY ASPECT OF THE GAME FOR YOU

## How Does It Look?

If you have none of these 5 debuffs (ignite, freeze, shock, bleed, poison) then you see nothing! Here's an image with all of them showing as if you were affected by them

![alt text](https://github.com/ExiledCrab/Reactable_Debuff_Overlay/blob/master/example.png?raw=true)

## How do I use it?
Head over to the [releases page](https://github.com/ExiledCrab/Reactable_Debuff_Overlay/releases) and grab the .exe from the newest version. Thats it!

When you run the .exe you'll see that it shows up running in the taskbar. You can just right click to close it whenever you dont need it open anymore.

## I don't want an exe, I wanna run the source code myself for safety
- Clone this repo
- setup your .venv
- pip install -r requirements.txt

and youre ready to just run main.py

## Current Caveats
* Windows only
* You MUST play PoE in `windowed` or `windowed fullscreen` graphics mode
* only tested to work on 1920x1080 resolution (what i play at, scaling is next thing that I'll be building out)
* Current performance isn't great. It updates about 7-8 times a second and your FPS takes a bit of a hit. (My potato machine is still above 100fps on avg but YMMV)
* No customization unless you like programming, another thing that I want to add in the future
* This was made in a couple hours, it shows lul

## This is witchcraft, how does it work?

Every update the overlay does, it grabs your PoE screen as a screenshot, then uses opencv to try and 'find' the debuff icons on your screen. After that im using pygame to draw an 'invisible' window overtop of your poe window (why it requires you to NOT use fullscreen) and if a debuff was found on the current update, it draws a small debff icon in the invisible window near where your character is. 

## Support Me
Do you love me for this? Want to support me?
Then just say hi or thanks on twitter [@ExiledCrab](https://twitter.com/ExiledCrab) and tell your fellow exiles about this tool

If you feel like going above & beyond to tip me beer/snacks money:
- Bitcoin Wallet: bc1qat7uvk2hz7g5y2fmfwhrl99zxm0v6pda3pap8h
- ETH Wallet: 0x1E2Ca68ee90003bDbeFe8a3176C280d0F066CFA0


## Contributing
If you find any terrible bugs or have ways of improving this, please open an issue and provide as much info as you can about what happened. (Screenshots are a huge bonus) 

## The Icons
Icons displayed are from [icons8](https://icons8.com)

## License
No license ATM
