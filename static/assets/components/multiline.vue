<template>
    <div style="height:auto">
        <div id = "wrapper" class="multi-line-wrapper">
        </div>
    </div>
</template>

<script>

export default {
    name: 'multiline',
    props: {
        year_val: {
            type: Array,
            default: []
        }
    },
    data() {
        return {

        }
    },
    watch: {
        year_val: function(newVal, oldVal){
            if (newVal != oldVal) {
            this.year_val = newVal;
            console.log('Watch data:' + JSON.stringify(newVal[0]));
            this.drawMultiLine();
            }
        }
    },
    methods:
    { 
        // Draw the multi line graph 
        drawMultiLine(){
            //Remove the existing graph, if it exists
            d3.select("#wrapper").select("svg").remove();

            
                // Set the dimensions of the canvas / graph
            var margin = {top: 30, right: 20, bottom: 30, left: 50},
                width = 600 - margin.left - margin.right,
                height = 300 - margin.top - margin.bottom;
            
            // Get the data
                var data = this.year_val;
                console.log('Data: ' + JSON.stringify(data[0]));
            // Parse the date / time
            var parseDate = d3.time.format("%m %Y").parse; 

            // change the format of the date variables
            data.forEach(function (d) {
                if (!(d.date instanceof Date)) {
                    d.date = parseDate(d.date);
                }       
                d.price = +d.price;
            });

            data.sort((a, b) => (a.date > b.date) ? 1 : -1);

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
            this.svg = d3.select('#wrapper')
                .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
            
                
            this.line = this.svg.append("g")
                        .attr("transform", 
                        "translate(" + margin.left + "," + margin.top + ")");

            

                // Scale the range of the data
                x.domain(d3.extent(data, function(d) { return d.date; }));
                y.domain([0, d3.max(data, function(d) { return d.price; })]); 

                // Nest the entries by symbol
                /*var dataNest = d3.nest()
                    .key(function(d) {return d.date;})
                    .entries(data);*/

                // Loop through each symbol / key
                //dataNest.forEach(function(d) {

                this.line.append("path")
                        .attr("class", "line")
                        .attr("d", priceline(data)); 

                //});

                // Add the X Axis
                this.line.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis);

                // Add the Y Axis
                this.line.append("g")
                    .attr("class", "y axis")
                    .call(yAxis);

            }
        }
    
}
</script>

<style> /* set the CSS */

body { font: 12px Arial;}

#wrapper path { 
    stroke: steelblue;
    stroke-width: 2;
    fill: none;
}

#wrapper .axis path,
#wrapper .axis line {
    fill: none;
    stroke: grey;
    stroke-width: 1;
    shape-rendering: crispEdges;
}

#wrapper .legend {
    font-size: 16px;
    font-weight: bold;
    text-anchor: middle;
}

</style>
