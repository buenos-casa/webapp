<template>
    <div style="height:auto">
        <div class="map-wrapper">
        </div>
    </div>
</template>



<script>

export default {
    mounted: function() {
        this.drawMap();
    },
    props: {
        barrio: {
            type: Number,
            required: true
        },
        mapname: {
            type: String,
            required: true
        },
        plot_points: {
            type: Array,
            required:false
        },
        lat: {
            type: Number,
            required: true
        },
        lon: {
            type: Number,
            required: true
        },
        dims: {
            type: Object,
            default: {'x': 500, 'y': 500}
        }
    },
    watch: {
        plot_points: function(newVal, oldVal) {
            this.drawHeatmap();
        }
    },
    methods: {
        drawHeatmap() {
            this.mapLayer.selectAll("circle").remove();
            if(this.plot_points.length > 0) {

                const max_val = 75000; // Math.max.apply(Math, this.plot_points.map(function(o) {return o.hue;}));
                const min_val = 495000; // Math.min.apply(Math, this.plot_points.map(function(o) {return o.hue;}));

                const colours = [
                    '#A67244',
                    '#AB794E',
                    '#B08158',
                    '#B58962',
                    '#BA916D',
                    '#BF9977',
                    '#C4A081',
                    '#C9A88C',
                    '#CEB096',
                    '#D3B8A0',
                    '#D9C0AB'
                ].reverse();

                var heatmapColour = d3.scale.linear()
                .domain(d3.range(0, 1, 1.0 / (colours.length - 1)))
                .range(colours);

                var c = d3.scale.linear().domain(d3.extent(this.plot_points.map(function(o) {return o.hue;}))).range([0,1]);

                const proj = this.projection;
                this.mapLayer.selectAll("circle")
                        .data(this.plot_points)
                        .enter()
                        .append("circle")
                        .attr("cx", function(d) {
                            // console.log(proj([d.lon, d.lat]));
                            return proj([d.lon, d.lat])[0];
                        })
                        .attr("cy", function (d) {
                            return proj([d.lon, d.lat])[1];
                        })
                        .attr("r", "1px")
                        .attr("fill", function(d) {return heatmapColour(c(d.hue))});
            }
        },
        drawMap() {
            var vue_ref = this;
            // Set svg width & height
            let centered = undefined;
            const size = {
                height: vue_ref.dims.y,
                width: vue_ref.dims.x
            };

            this.projection = d3.geo.equirectangular()
                                    .scale(125000)
                                    .center([vue_ref.lon, vue_ref.lat])
                                    .translate([size.width / 2, size.height / 2]);

            const path = d3.geo.path()
                                .projection(this.projection);

            this.svg = d3.select(this.$el.children[0])
                .append('svg')
                .attr('width', size.width)
                .attr('height', size.height);


            // Add background
            this.svg.append('rect')
                .attr('class', 'background')
                .style('fill', 'none')
                .attr('width', size.width)
                .attr('height', size.height);

            const g = this.svg.append('g');

            const effectLayer = g.append('g')
                                .classed('effect-layer', true);
            
            const mapLayer = g.append('g')
                            .classed('map-layer', true);

            this.mapLayer = mapLayer;
            
            // Load map data
            const geoJsonUrl = '/static/geojson/' + this.mapname + '.json';

            d3.json(geoJsonUrl, function(error, mapData) {
                vue_ref.j_features = mapData.features;

                var features = vue_ref.j_features;

                // Draw each province as a path
                mapLayer.selectAll('path')
                    .data(features)
                    .enter().append('path')
                    .attr('d', path)
                    .style('fill', function(d) {
                        if(d.properties.barrio === vue_ref.barrio) {
                            return "#3b6d8c";
                        } else {
                            return "#e1e2eb";
                        }
                    })
                    .style('stroke', "#3b6d8c")
                    .style('stroke-width', '2px')
                    .attr('vector-effect', 'non-scaling-stroke')
                    .each(onLoad)
            });

            function onLoad(d) {
                if(d.properties.barrio === vue_ref.barrio) {
                    var x, y, k;
                    // Compute centroid of the selected path
                    var centroid = path.centroid(d);
                    console.log(centroid);
                    x = centroid[0];
                    y = centroid[1];
                    k = 4;

                    vue_ref.drawHeatmap();

                    // Zoom
                    g.transition()
                     .attr('transform', 
                           'translate(' + size.width / 2 + ',' + size.height / 2 + ')scale(' + k + ')translate(' + -x + ',' + -y + ')'
                           );
                }
            }
        }
    }
}

</script>

<style>
    .map-wrapper {
        .background {
            fill: none;
            pointer-events: all;
        }
        .map-layer {
            fill: whitesmoke;
            stroke: #021019;
            stroke-width: 1px;
        }
         path { 
        stroke: black;
        stroke-width: 2;
        fill: nonee;
        }
    }
</style>
