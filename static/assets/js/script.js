// Include libraries
/*import Vue from 'vue'
import axios from 'axios'
import WebFont from 'webfontloader'
import Mapbaires from '../components/mapbaires.vue'
import {
  // Flow Of transition
  d3SankeyCircular,

  // Time Serie
  d3Timelion,
  d3Timeline,

  // Basic
  d3Pie,
  d3Line,
  d3Metric,
  d3MultiLine,
  d3HorizontalBar,
  d3VerticalBar,
  d3GroupedArea,
  d3Area,
  d3Circle,

  // Functional
  d3Player,
  d3HorizontalSlider,
  d3VerticalSlider,

  // Layout
  d3Sunburst,
  d3Tree,
  d3Pack,
  d3Cluster,
  d3ICicleVertical,
  d3ICicleHorizontal,

  // Leaflet
  d3LChoropleth,
  d3LHeat
} from 'd3-vs';

console.log('It\'s running!');
// Init Google Fonts
WebFont.load({
  google: {
    families: ['Open+Sans:300,400']
  }
})
*/
// Following this tutorial: https://travishorn.com/interactive-maps-with-vue-leaflet-5430527353c8

// Init Vue app
<<<<<<< HEAD
const kickstart_app = new Vue({
  el: '#app',
  data: { map: null,
    tileLayer: null,
    layers: [], },
  mounted() { 
    this.initMap();
    this.initLayers();},
  methods: { initMap() {
    //generating map of Buenos Aires
    this.map = L.map('map').setView([-34.652889, -58.442420], 10);
    this.tileLayer = L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png', {
    maxZoom: 18,
	  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>'
    });

    this.tileLayer.addTo(this.map);

    //this.geocoder = L.Mapzen.geocoder('mapzen-fkPfGup');
    //this.geocoder.addTo(map);
  },
  initLayers() {},},
=======
const vue_app = new Vue({
  el: '#app',
  components: {
    Mapbaires
  }
>>>>>>> dev
});
