/*
 * A general purpose utility class full of static functions.
 *
 * Author: Owain Jones [github.com/doomcat]
 */

utils = {

    /* Calculates the Levenshtein Distance between two strings.
     * This allows you to do 'fuzzy' comparisons between things.
     *
     * Returns the distance between them as an integer. */
    levenshtein: function(first, second) {
        // TODO: Complete this function.
        return 0;
    }
};

/* Add some nice pythonic things that I'm used to :) */
/* TODO:    Look up the most efficient way to do these things in JS!
 *          (I'm sure Array.slice comes into play) */

String.prototype.startswith = function(str) {
    if(this === str) {
        return true;
    } else if(this.length < str.length) {
        return false;
    } else if(this.substr(0,str.length) === str) {
        return true;
    }
    return false;
};

String.prototype.endswith = function(str) {
    if(this === str) {
        return true;
    } else if(this.length < str.length) {
        return false;
    } else if(this.substr(this.length, -str.length) === str) {
        return true;
    }
    return true;
};

String.prototype.contains = function(str) {
    var i;
    if(this === str) {
        return true;    
    } else if(this.length < str.length) {
        return false;
    } else {
        for(i=0; i<this.length; i++) {
            if(this.substr(i).startswith(str)) {
                return true;
            } else if(this.substr(-i).endswith(str)) {
                return true;
            }
        }
    }
    return false;
};

/* I am super lazy and pythonic */
function pass() {};
