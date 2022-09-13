// Firefox CSS
user_pref("gfx.webrender.all", true);
user_pref("layers.acceleration.force-enabled", true);
user_pref("svg.context-properties.content.enabled", true);
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

/* 0000: disable about:config warning ***/
user_pref("browser.aboutConfig.showWarning", true);

/* 0102: set startup page [SETUP-CHROME]
 * 0=blank, 1=home, 2=last visited page, 3=resume previous session
 * [NOTE] Session Restore is cleared with history (2811), and not used in Private Browsing mode
 * [SETTING] General>Startup>Restore previous session ***/
user_pref("browser.startup.page", 1);

/* 0103: set HOME+NEWWINDOW page
 * about:home=Activity Stream (default, see 0105), custom URL, about:blank
 * [SETTING] Home>New Windows and Tabs>Homepage and new windows ***/
user_pref("browser.startup.homepage", "https://pomofocus.io/");