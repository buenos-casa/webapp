<template>
    <div style="height:auto">
        <div class="multi-line-wrapper">
        </div>
    </div>
</template>

<script>

export default {
    mounted: function(){
        this.drawMultiLine();
    },
    props: {
        year_val: Array,
    },
    data(){
        return
    },
    methods:
    {
        drawMultiLine(){
            // Set the dimensions of the canvas / graph
        var margin = {top: 30, right: 20, bottom: 30, left: 50},
            width = 600 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        // Parse the date / time
        var parseDate = d3.time.format("%m %Y").parse; 

        // Set the ranges
        var x = d3.time.scale().range([0, width]);
        var y = d3.scale.linear().range([height, 0]);

        // Define the axes
        var xAxis = d3.svg.axis().scale(x)
            .orient("bottom").ticks(5);

        var yAxis = d3.svg.axis().scale(y)
            .orient("left").ticks(5);

        // Define the line
        var priceline = d3.svg.line()
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.price); });
            
        // Adds the svg canvas
        this.svg = d3.select(this.$el.children[1])
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform", 
                    "translate(" + margin.left + "," + margin.top + ")");

            // Get the data
            var data = this.year_val;

            // Scale the range of the data
            x.domain(d3.extent(data, function(d) { return d.date; }));
            y.domain([0, d3.max(data, function(d) { return d.price; })]); 

            // Nest the entries by symbol
            var dataNest = d3.nest()
                .key(function(d) {return d.symbol;})
                .entries(data);

            // Loop through each symbol / key
            dataNest.forEach(function(d) {

                svg.append("path")
                    .attr("class", "line")
                    .attr("d", priceline(d.values)); 

            });

            // Add the X Axis
            this.svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            // Add the Y Axis
            this.svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);

        }
        }
    
}
</script>