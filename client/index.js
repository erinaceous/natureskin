/*
 * This file is an index of the scripts we still have to load.
 * When loaded, it proceeds to load these other scripts by inserting
 * <script> elements in the <head> of the DOM.
 *
 */
var script;

scripts = [
    "phonegap.js",
    "cordova.js",
    "lib/jquery-1.9.1.js",
    "lib/jquery.mobile-1.3.0/jquery.mobile-1.3.0.js",
    "lib/jquery.mobile.simpledialog2.js",
    "lib/simplify.js",
    "res/utils.js",
    "res/database.js",
    "res/normalize.js",
    "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry&region=GB&sensor=true&key=AIzaSyCZpQAo0USwbOMZEX4Hb3OHISQktfzza2s",
    "res/app.js",
    "data/magaonb.json"
];

for(script in scripts) {
    script = scripts[script];
    //tag = document.createElement('script');
    //tag.type = "text/javascript";
    //tag.src = script;
    try{ 
        //document.getElementsByTagName('head')[0].appendChild(tag);
        document.write('<' + 'script src="' + script + '"' +
                       ' type="text/javascript"><' + '/script>');
    } catch(e) {

    }
}
