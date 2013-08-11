============================== 
Django-Critique Static Media
==============================

**SASS**
---------
Critique's stylesheets are developed using `SASS <http://sass-lang.com/>`_ and `Compass <http://compass-style.org>`_. SASS is a CSS Preprocessor and Compass is a CSS Authoring Framework that utilizes SASS to work its magic. To ensure maximum compatibility, always develop using the most recent releases of both SASS and Compass.

**CSS**
---------
All .scss files are compiled to CSS that is perfectly usable completely independent of SASS and Compass. If you're going to directly edit the CSS files be sure you DO NOT run 'compass compile' or 'compass watch' because all CSS files will be recompiled from the .scss and any added code will be overwritten with no warning. In fact, if you are planning to directly edit any of Critique's CSS files it is advised that you remove the SASS directory and config.rb files from your install.

**config.rb**
---------
This file is where all of the project's SASS settings are configured. There are more detailed explanations of each item included in the file itself. The Compass documentation provides a great `reference <http://compass-style.org/help/tutorials/configuration-reference>`_ for all of the configuration options available to this file.

**Contributions**
---------
If you'd like to contribute a new Critique theme or a bug fix to one of the existing themes, please make your changes using the .scss stylesheets or we won't be able to accept them.