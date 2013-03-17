var natureskin = {
    api: {
        query: function(query, callback) {
            string = escape(JSON.stringify(query));
            $.ajax({
                dataType: "json",
                url: "//ns.odj.me/api/_find?criteria="+string,
                success: callback
            });
        }
    }
};
