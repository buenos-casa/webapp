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
        mapname: {
            type: String,
            required: true
        },
        barrios_val: Array,
        heatmap_val: {
            type: Array,
            required:false,
            default: () => []
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
        barrios_val: function(newVal, oldVal) {
            var max_val = Math.max(newVal);
            var min_val = Math.min(newVal);

            //var colours = ["#3B6D8C", "#638CA6", "#F2B705", "#D9923B", "#A67244"];
            //var colours = ['#3b6d8c', '#00859c', '#F2B705", "#D9923B"', '#1aad70', '#7fb940', '#a3b42b', '#c4ad1f', '#e3a326', '#d69531', '#c7893a', '#b77d40', '#a67244'];
             //var colours = ['#ffffff', '#fceafb', '#ffd1e3', '#ffbbb6', '#ffaf7f', '#faa965', '#f0a548', '#e3a326', '#d69531', '#c7893a', '#b77d40', '#a67244']
             var colours = ['#e7e7ee', '#ccd0de', '#afbbce', '#90a6bd', '#7e9ab3', '#6c8fa9', '#59849f', '#527e9a', '#4a7895', '#437391', '#3b6d8c']

            var heatmapColour = d3.scale.linear()
            .domain(d3.range(0, 1, 1.0 / (colours.length - 1)))
            .range(colours);

            var c = d3.scale.linear().domain(d3.extent(newVal)).range([0,1]);

            var map_layer = this.svg.selectAll("g.map-layer").selectAll("path");
            map_layer.transition(500).style('fill', function(d) {
                return heatmapColour(c(newVal[d.properties.barrio]));
            });
        },
        heatmap_val: function(newVal, oldVal) {
            if(this.selected_province) {
                this.drawHeatmap();
            }
        }
    },
    data() { 
        return {
            selected_province: undefined,
        }
    },
    methods: {
        openInfo(province) {
            this.$parent.$emit('province-chosen', {'b_id': province.barrio, 'commune': province.commune});
            this.selected_province = province;
            this.drawHeatmap();
        },
        closeInfo() {
            this.$parent.$emit('province-chosen', undefined);
            this.selected_province = undefined;
            this.mapLayer.selectAll("circle").remove();
        },
        drawHeatmap() {
            this.mapLayer.selectAll("circle").remove();
            if(this.heatmap_val.length > 0 && this.heatmap_val[this.selected_province.barrio]) {
                const proj = this.projection;
                this.mapLayer.selectAll("circle")
                        .data(this.heatmap_val[this.selected_province.barrio])
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
                        .attr("fill", "red")
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
                .attr('height', size.height)
                .on('click', clicked);

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
                    .attr('vector-effect', 'non-scaling-stroke')
                    .style('fill', 'whitesmoke')
                    .style('stroke', '#3B6D8C')
                    .style('stroke-width', '2px')
                    .on('mouseover', mouseover)
                    .on('mouseout', mouseout)
                    .on('click', clicked)
            });

            function clicked(d) {
                var x, y, k;
                
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

                d3.select(this).style('opacity', '1.0');

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

                d3.select(this).style('opacity', '0.75');

                d3.select(this).transition()
                               .duration(250)
                               .attr('transform', 'scale(' + scale + ')translate(' + x + ',' + y + ')');
            }

            function mouseout(d){
                if (centered == d) {
                    return;
                }
                // De-highlight province
                d3.select(this).style('opacity', '1.0');
                d3.select(this).transition()
                               .duration(250)
                               .attr('transform', 'scale(' + 1.0 + ')');

            }
        }
    }
}

</script>

<style>
    #map-wrapper .background {
            fill: none;
            pointer-events: all;
    }
    #map-layer .axis path {
            fill: whitesmoke;
            stroke: #021019;
            stroke-width: 2px;
        }
</style>
