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

            var colours = ["#6363FF", "#6373FF", "#63A3FF", "#63E3FF", "#63FFFB", "#63FFCB",
                        "#63FF9B", "#63FF6B", "#7BFF63", "#BBFF63", "#DBFF63", "#FBFF63", 
                        "#FFD363", "#FFB363", "#FF8363", "#FF7363", "#FF6364"];

            var heatmapColour = d3.scale.linear()
            .domain(d3.range(0, 1, 1.0 / (colours.length - 1)))
            .range(colours);

            var c = d3.scale.linear().domain(d3.extent(newVal)).range([0,1]);

            var map_layer = this.svg.selectAll("g.map-layer").selectAll("path");
            map_layer.style('fill', function(d) {
                console.log(heatmapColour(c(newVal[d.properties.barrio])));
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

            const color = d3.scale.linear()
                                    .domain([1, 20])
                                    .clamp(true)
                                    .range(['#08304b', '#08304b']);

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
            
            console.log(this.mapname);

            // Load map data
            const geoJsonUrl = '/static/geojson/' + this.mapname + '.json';

            d3.json(geoJsonUrl, function(error, mapData) {
                vue_ref.j_features = mapData.features;

                console.log(vue_ref.j_features);

                var features = vue_ref.j_features;

                // Update color scale domain based on data
                color.domain([0, d3.max(features, nameLength)]);

                // Draw each province as a path
                mapLayer.selectAll('path')
                    .data(features)
                    .enter().append('path')
                    .attr('d', path)
                    .attr('id', function(d){
                        return '#b' + d.properties.barrio;
                    })
                    .attr('vector-effect', 'non-scaling-stroke')
                    .style('fill', fillFn)
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
                } else {
                    x = size.width / 2;
                    y = size.height / 2;
                    k = 1;
                    centered = null;
                    vue_ref.closeInfo();
                }

                // Highlight the clicked province
                mapLayer.selectAll('path')
                    .style('fill', function(d){
                    return centered && d===centered ? '#D5708B' : fillFn(d);
            });

            // Zoom
            g.transition()
                .duration(750)
                .attr('transform', 'translate(' + size.width / 2 + ',' + size.height / 2 + ')scale(' + k + ')translate(' + -x + ',' + -y + ')');
            }

            function mouseover(d){
                // Highlight hovered province
                d3.select(this).style('fill', '#1483ce');
                if(d) {
                    vue_ref.selectProvince(d.properties);
                }
            }

            function mouseout(d){
                vue_ref.selectProvince(undefined);
                // Reset province color
                mapLayer.selectAll('path')
                    .style('fill', (d) => {
                    return centered && d===centered ? '#D5708B' : fillFn(d);
                    });
            }

            // Get province name length
            function nameLength(d){
                const n = nameFn(d);
                return n ? n.length : 0;
            }

            // Get province name
            function nameFn(d){
                return d && d.properties ? d.properties.barrios : null;
            }

            // Get province color
            function fillFn(d){
                return color(nameLength(d));
            }
        }
    }
}

</script>

<style scoped>
.map-wrapper {
    .province-title {
        position: absolute;
        top: 50px;
        left: 150px;
        color: white;
    }
    .province-info {
        background: white;
        position: absolute;
        top: 150px;
        right: 20px;
        height: 400px;
        width: 300px;
    }
    .background {
        fill: #021019;
        pointer-events: all;
    }
    .map-layer {
        fill: #08304b;
        stroke: #021019;
        stroke-width: 1px;
    }
}
</style>
