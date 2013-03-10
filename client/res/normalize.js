/*
 * A library for normalizing dictionaries in Javascript.
 * Where "normalizing" means making key names equal by renaming keys,
 * merging objects which contain equal key-value pairs, and transforming
 * values by running functions on them.
 *
 * the Neurotypical class also takes a dictionary to the constructor,
 * allowing you to configure exactly how you want stuff to be normalized.
 *
 * Author: Owain Jones [github.com/doomcat]
 */

normalizer = {
    clone: function(object) {
        return JSON.parse(JSON.stringify(object));
    },

    toTitleCase: function(string) {
        return string.replace(/\w\*/g, function(txt) {
            return txt.charAt(0).toUpperCase() +
                   txt.substr(1).toLowerCase();
        });
    },

    Neurotype: function(mappings, functions) {
        this.mappings = mappings;
        this.functions = functions;

        this.behave = function(object) {
            var mapping;
            var current;
            clone = normalizer.clone(object);
            for(mapping in this.mappings) {
                clone[this.mappings[mapping]] = clone[mapping];
            }
            for(mapping in this.functions) {
                clone[mapping] = this.functions[mapping](
                    clone[mapping], clone
                );
            }
            return clone;
        };
    }
};
