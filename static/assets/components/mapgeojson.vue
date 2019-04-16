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
        mapname: String,
        barrios_val: Array
    },
    watch: {
        barrios_val: function(newVal, oldVal) {
            console.log("changed");

            var max_val = Math.max(newVal);
            var min_val = Math.min(newVal);

            var colours = ["#3B6D8C", "#638CA6", "#F2B705", "#D9923B", "#A67244"];

            var heatmapColour = d3.scale.linear()
            .domain(d3.range(0, 1, 1.0 / (colours.length - 1)))
            .range(colours);

            var c = d3.scale.linear().domain(d3.extent(newVal)).range([0,1]);

            var map_layer = this.svg.selectAll("g.map-layer").selectAll("path");
            map_layer.transition(100).style('fill', function(d) {
                // console.log(heatmapColour(c(newVal[d.properties.barrio])));
                return heatmapColour(c(newVal[d.properties.barrio]));
            });
        }
    },
    data() { 
        return {

        }
    },
    methods: {
        selectProvince(province) {
            // this.province = province;
        },
        openInfo(province) {
            this.$parent.$emit('province-chosen', {'b_id': province.barrio, 'commune': province.commune});

        },
        closeInfo() {
            this.$parent.$emit('province-chosen', undefined);
        },
        drawMap() {
            var vue_ref = this;
            // Set svg width & height
            let centered = undefined;
            const mapCenter = {
                lat: -34.6,
                lng: -58.4
            };
            const size = {
                height: 500,
                width: d3.select('.map-wrapper').node().getBoundingClientRect().width,
            };

            const projection = d3.geo.equirectangular()
                                    .scale(100000)
                                    .center([mapCenter.lng, mapCenter.lat])
                                    .translate([size.width / 2, size.height / 2]);

            const path = d3.geo.path()
                                .projection(projection);

            this.svg = d3.select(this.$el.children[0])
                .append('svg')
                .attr('width', size.width)
                .attr('height', size.height);


            // Add background
            this.svg.append('rect')
                .attr('class', 'background')
                .attr('width', size.width)
                .attr('height', size.height)
                .on('click', clicked);

            const g = this.svg.append('g');

            const effectLayer = g.append('g')
                                .classed('effect-layer', true);
            
            const mapLayer = g.append('g')
                            .classed('map-layer', true);
            
            // console.log(this.mapname);

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
                    .attr('vector-effect', 'non-scaling-stroke')
                    .style('fill', '#ffffff')
                    .on('mouseover', mouseover)
                    .on('mouseout', mouseout)
                    .on('click', clicked)
            });

            function clicked(d) {
                var x, y, k;

                // d3.select(this).transition()
                //                .duration(750)
                //                .style("stroke-width: 5; stroke:black;")

                // Compute centroid of the selected path
                if (d && centered !== d) {
                    var centroid = path.centroid(d);
                    x = centroid[0];
                    y = centroid[1];
                    k = 4;
                    centered = d;
                    vue_ref.openInfo(d.properties);
                    console.log(d);
                } else {
                    x = size.width / 2;
                    y = size.height / 2;
                    k = 1;
                    centered = null;
                    vue_ref.closeInfo();
                }

                d3.select(this).transition()
                               .duration(750)
                               .attr('transform', 'scale(' + 1.0 + ')')

                // Zoom
                g.transition()
                    .duration(750)
                    .attr('transform', 'translate(' + size.width / 2 + ',' + size.height / 2 + ')scale(' + k + ')translate(' + -x + ',' + -y + ')');
            }

            function mouseover(d){
                if(centered == d){
                    return;
                }
                var scale = 1.05
                // Highlight hovered province
                var centroid = path.centroid(d);
                var x = (1 - scale) * centroid[0];
                var y = (1 - scale) * centroid[1];

                d3.select(this).transition()
                               .duration(750)
                               .attr('transform', 'scale(' + scale + ')translate(' + x + ',' + y + ')');
            }

            function mouseout(d){
                if (centered == d) {
                    return;
                }
                // De-highlight province
                d3.select(this).transition()
                               .duration(750)
                               .attr('transform', 'scale(' + 1.0 + ')');
            }
        }
    }
}

</script>

<style scoped>
    .map-wrapper {
        .background {
            fill: #021019;
            pointer-events: all;
        }
        
        .map-layer {
            fill: #08304b;
            stroke: #021019;
            stroke-width: 1px;
        }

        path.map-layer:hover {
            transform: scale(2.0);
            -ms-transform: scale(2.0);
            -webkit-transform: scale(2.0);
        }
    }
</style>
