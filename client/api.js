var natureskin = {
    api: {
        query: function(query, callback) {
            string = escape(JSON.stringify(query));
            $.ajax({
                dataType: "json",
                url: "//ns.odj.me/api/areas/_find?criteria="+string,
                success: callback
            });
        },
        find_near: function(lon, lat, callback, radius) {
            if(!radius) { radius = 10; }
            var miles = radius / 3963.192;
            natureskin.api.query({
                "center": {"$within": {"$centerSphere": [[lon, lat], miles]}}
            }, callback);
        }
    }
};
