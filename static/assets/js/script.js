// Include libraries
import Vue from 'vue'
import axios from 'axios'
import WebFont from 'webfontloader'
import Mapgeojson from '../components/mapgeojson.vue'
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
    families: ['Alegreya:300,400']
  }
})

// Following this tutorial: https://travishorn.com/interactive-maps-with-vue-leaflet-5430527353c8

// Init Vue app
const vue_app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  components: {
    Mapgeojson,
    d3Circle,
    d3Line
  },
  data() {
    return {
      result: [],
      communes: [],
      barrios: undefined,
      census: [],
      barrios_val: [],
      bar_avg: null,
      province: "Barrio"
    }
  },
  methods: {
    getCommunes() {
      axios.get('/api/commune/')
           .then(response => {
             this.result = response.data.data;
           })
           .catch(error => {
             console.log(error);
           });
    },
    getCommuneCensus(commune) {
      axios.get('/api/census/' + commune)
           .then(response => {
             this.census = response.data.data;
           })
           .catch(error => {
             console.log(error);
           })
    },
    getBarrios() {
      axios.get('/api/barrio/')
           .then(response => {
             this.barrios = response.data.data;
           })
           .catch(error => {
             console.log(error);
           })
    },
    getAvgBarrioValUS(b_id) {
      if (this.barrios_val.length <= 0) {
        axios.get('/api/property/us_val/avg/')
            .then(response => {
              this.barrios_val = response.data.data;
              this.bar_avg = this.barrios_val[b_id];
            })
            .catch(error => {
              console.log(error);
            })
          }
      else {
        this.bar_avg = this.barrios_val[b_id];
      }
    },
    getBarriosVal(endpoint) {
      axios.get(endpoint)
           .then(response => {
            this.barrios_val = response.data.data;
           })
           .catch(error => {
             console.log(error);
           })
    },
    onProvinceChange: function(province) {
      if(province) {
        this.province = this.barrios[province.b_id];
      } else {
        this.province = "Barrio";
      }
    }
  },
  mounted: function() {
    this.$on('province-chosen', this.onProvinceChange);
    this.getBarriosVal('/api/property/us_val/avg/');
    if (document.querySelectorAll('.communes').length > 0) {
      this.getCommunes();
      this.getBarrios();
    }
    if (document.querySelectorAll('.communasData').length > 0) {
      this.getCommuneCensus(1);
    }
  }
});
