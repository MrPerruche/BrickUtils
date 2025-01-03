# BRICKUTILS IS NO LONGER MAINTAINED

**AFTER CAREFUL CONSIDERATION, I HAVE DECIDED TO ABANDON THIS PROJECT, AS I HAVE LOST INTEREST IN IT.**
**IT HAS ALSO BECOME TOO DIFFICULT TO MAINTAIN BOTH THE PROJECT AND THE OUTDATED VERSION OF BRCI (BRCI 3.54).**

**IF YOU ARE INTERESTED IN MAINTAINING IT, PLEASE CONTACT ME ON DISCORD (@perru_). THANK YOU FOR YOUR UNDERSTANDING.**

# BrickUtils

BrickUtils only supports Windows. Other OS will cause a variety of issues.

BrickUtils is only on GitHub to share it and it's code.
Suggestions are welcome but pull requests are not accepted.

How to install?
- (No video yet)
- Install the latest version of BrickUtils
- Install python on https://www.python.org/downloads/release/python-3124/
(If you don't know which to pick, try Windows Installer (64-bit))
- Go in Windows powershell and type `py -3.12 -m pip install Pillow`
- Installation is done. Run `main.py` to start the program

PLEASE READ THE IMPORTANT INFORMATION MENU! IT IS AVAILABLE IN MULTIPLE LANGUAGES.

If you have any feedback, found a bug, need help, or more, join the BRCI Discord server: https://discord.gg/invite/sZXaESzDd9

## Changelog

### Under consideration for future updates
- None

### Update D8
Last major update: end of beta & creation editor improvements
- Revamp creation editor UX.
- Restrict scaling to always scale each axis equally.
- Add build rotation (in creation editor).
- Add duplicated bricks deletion (in creation editor).
- Add connections edition (in creation editor).
- Fixed issue with connections menu always claiming back was previously connected.
- \*Note: From now on I will work a lot less on BrickUtils. Only maintenance updates and fixes will be made.
- \*as such, the light bar generator is cancelled and is no longer accessible*.
- \*PRs will from now on be accepted if you wish working on BrickUtils (I doubt that).

### Update D7
Important fixes:
- Updated BRCI to C54 (C51 -> C54), featuring bugfixes and reducing data loss risks.
- BrickUtils now refuses to generate anything when no project is provided, fixing a severe issue regarding data loss.
- Removed creation editor temporarily as it's soon going to be revamped.
- BrickUtils is no longer configured to port any files to Brick Rigs by default.
- Added settings reinitialization in the settings menu.
- \* BrickUtils D2 and newer fully support Python 3.12.5.
- \* BrickUtils D2 and newer fully support Brick Rigs 1.7.4.

### Update D6
Added encryption / decryption:
- Added a basic .brv (en/de)cryptor.
- Added a warning regarding rotation not working in the edit menu.
- Added to BrickUtils' window its own icon.
- Started working on lightbar generation.
- Fixed incorrect input labels when editing the selected project in the brick generator.
- Fixed incorrect punctuation in the changelog.
- \* BrickUtils D2 and newer fully support Brick Rigs 1.7.3b.

### Update D5
Various fixes:
- Fixed fatal error when inputting nothing in Main menu > Lightbar generator > Import from.
- Fixed fatal error when attempting to preview a lightbar with no stages.
- Fixed fatal error when giving an incorrect color.
- Added "code injector" to developer tools script.

### Update D4
Pre beta release changes & improvements:
- Added optional `force_settings.txt` file to run arbitrary code on startup.
- Clearing terminal now use escape codes, which are faster.
- Revised lightbar preview menu.
- A few fixes.
- Finally enabled `safe_mode` by default.
