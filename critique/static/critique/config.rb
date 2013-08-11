#
# This file is only needed for Compass/Sass integration. If you are not using
# Compass, you may safely ignore or delete this file.
#

# To compress all CSS, change to production mode before deploying.
environment = :development
#environment = :production

# If you use firesass, turn on firesass enabled debug info
firesass = false
#firesass = true

# Location of the static resources.
css_dir         = "css"
sass_dir        = "sass"
images_dir      = "images"
javascripts_dir = "js"

# You can select your preferred output style here (can be overridden via the command line):
# output_style = :expanded or :nested or :compact or :compressed
output_style = (environment == :development) ? :expanded : :compressed

# To enable relative paths to assets via compass helper functions.
relative_assets = false

# To disable debugging comments that display the original location of your selectors. Uncomment:
#line_comments = false

# Pass options to sass. For development, we turn on the FireSass-compatible
# debug_info if the firesass config variable above is true.
sass_options = (environment == :development && firesass == true) ? {:debug_info => true} : {}
