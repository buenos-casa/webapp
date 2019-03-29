// Include libraries
/*import Vue from 'vue'
import axios from 'axios'
import WebFont from 'webfontloader'

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
});
