# include("$BOARD_DIR)/manifest.py")
freeze("$(BOARD_DIR)/modules")

# include("$(PORT_DIR)/boards/manifest.py")
freeze("$(PORT_DIR)/modules")
include("$(MPY_DIR)/extmod/asyncio")

# Useful networking-related packages.
require("bundle-networking")

# Require some micropython-lib modules.
require("neopixel")
require("upysh")
require("aiorepl")

package("PyNAU7802", files=["__init__.py", "constants.py",
        "nau7802.py"], base_path="modules/PyNAU7802")

module("mqtt_as.py", base_path="modules/micropython-mqtt/mqtt_as")

# These two need to be at the root
module("main.py", base_path="src")
module("boot.py", base_path="src")

package("app", base_path="src")
