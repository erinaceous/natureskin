/* A database class for the natureskin client.
 * Since most of the data is loaded from .json files kept with the app,
 * we want to be able to load those files into an already existing
 * database and do queries on the data.
 *
 * Author: Owain Jones [github.com/doomcat]
 */

database = {
    layers: {},
    hasUpdated: false,

    /* Load an area's meta data into memory */
    /* data/index.js calls this function */
    load_meta: function(data, onLoad) {
        var key;
        for(key in data.layers) {
            this.layers[key] = data.layers[key];
            this.layers[key].areas = [];
        }
        if(typeof(onLoad) === "function") {
            onLoad();
        }
        this.hasUpdated = true;
    },

    /* Load an area's point data into memory */
    /* data/.json calls this function */
    load_areas: function(key, data, onLoad) {
        this.layers[key].areas = data;
        if(typeof(onLoad) === "function") {
            onLoad();
        }
        this.hasUpdated = true;
    },

    /* Add a single area into memory. */
    load_area: function(key, data, onLoad) {
        if(this.layers[key]) {
            this.layers[key].areas.push(data);
        } else {
            this.layers[key] = {"areas": [data]};
        }
        if(typeof(onLoad) === "function") {
            onLoad();
        }
        this.hasUpdated = true;
    },

    load_from_file: function(key, data, onLoad) {
        var object;
        for(object in data) {
            this.load_area(key, data[object]);
        }
        if(typeof(onLoad) === "function") {
            onLoad();
        }
        this.hasUpdated = true;
    },

    /* Unload a layer's areas from memory */
    unload: function(key) {
        this.layers[key].areas = null;
        this.hasUpdated = true;
    },

    /* Execute a query on the database. The query format is inspired by
     * MongoDB and other NoSQL databases: give it an object with keys
     * and values you're looking for.
     * Use a list of values to search for multiple values.
     * Use a value of {"$starts": "value"} / {"$ends": "value"} and
     * {"$like" "value"} to find 'similar' results to your query.
     * Use a value of {"$lt": "value"} / {"$gt": "value"} to do
     * comparisons.
     * Use a value of "$layer": "layer" to search for objects in a
     * specific layer.
     *
     * This is an asynchronous call - it runs as fast as possible, but
     * in a setInteval loop. This is to prevent it locking up the
     * app during intensive queries (e.g. bounds checking).
     * To get the result, define an 'onResult' function that will take
     * the results (a list of area objects) as its argument.
     *
     * Returns an anonymous function which, when called, will force the
     * query to stop and fire the onResult function. */
    query: function(query, onResult) {
        var index = 0;
        var length = 0;
        var i = 0;
        var layer;
        var objects = [];
        var object;
        if(typeof(onResult) === "function") {
            for(layer in this.layers) {
                for(object in this.layers[layer].areas) {
                    objects.push(this.layers[layer].areas[object]);
                }
            }
            _query(query, [], onResult, objects, index);
            return function() {
                /* TODO:    How do I stop setTimeout functions from
                 *          running remotely? */
            };
        } else {
            return function() {};
        }
    },

    /* Body of the query function. */
    _query: function(query, results, onResult, objects, index) {
        var layer;
        var object;
        var key;
        if(this.hasUpdated === true) {
            /* Database has been updated whilst we've been querying it!
             * So restart the query - discard our results so far. */
            objects = [];
            for(layer in this.layers) {
                for(object in this.layers[layer].areas) {
                    objects.push(this.layers[layer].areas[object]);
                }
            }
            _query(query, [], onResult, objects, 0);
        } else if(objects.length >= length-1) {
            onResult(results);
            return;
        }

        /* Do the actual query stuff */
        object = objects[index];
        for(key in query) {
            // if keys start with $ then they're metakeys
            if(key.startswith("$")) {
                // Do whatever comparison
            }
            else if(object.key === query.key) {
                results.push(object);
            }
        }

        /* Run again in the future. */
        setTimeout(function() {
            _query(query, results, onResult, length, index+1);
        }, 0);
    },

};
