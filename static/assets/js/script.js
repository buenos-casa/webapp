// Include libraries
import Vue from 'vue'
import axios from 'axios'
import WebFont from 'webfontloader'
import Mapgeojson from '../components/mapgeojson.vue'
import {
  // Basic
  d3Pie,
  d3Line,
  d3MultiLine,
  d3HorizontalBar,
  d3VerticalBar,
  d3Circle,

  // Functional
  d3HorizontalSlider,
  d3VerticalSlider,
} from 'd3-vs';

console.log('It\'s running!');
// Init Google Fonts
WebFont.load({
  google: {
    families: ['Alegreya:300,400']
  }
})

// Init Vue app
const vue_app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  components: {
    Mapgeojson,
    d3Pie,
    d3Circle,
    d3Line,
    d3HorizontalBar,
    d3MultiLine,
    d3HorizontalSlider,
    d3VerticalSlider
  },
  data() {
    return {
      vw: 'overview',
      st: 'pv',
      h_kind: 'purchase',
      barrios: undefined,
      census: [],
      barrios_val: [],
      heatmap_val: [],
      importance_val: [],
      multiline_mo_val: [],
      housing_summary: undefined,
      province: undefined,
    }
  },
  methods: {
    getBarrios() {
      axios.get('/api/barrio/')
           .then(response => {
             this.barrios = response.data.data;
           })
           .catch(error => {
             console.log(error);
           })
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
    getHeatmapVal(endpoint) {
      axios.get(endpoint)
           .then(response => {
            this.heatmap_val = response.data.data;
           })
           .catch(error => {
             console.log(error);
           })
    },
    getImportance(b_id, year) {
      var endpoint = '/api/importance/' + year + '/' + b_id;
      axios.get(endpoint)
           .then(response => {
             this.importance_val = response.data.data;
           })
           .catch(error => {
             console.log(error);
           })
    },
    getMonthly(kind) {
      var endpoint = undefined;
      var endpoint_a = undefined;
      if(this.province) {
        endpoint = '/api/' + kind + '/monthly/' + this.province.id;
        endpoint_a = '/api/' + kind + '/' + this.province.id;
      } else {
        endpoint = '/api/' + kind + '/monthly/0';
        endpoint_a = '/api/' + kind + '/0';
      }
      axios.get(endpoint)
           .then(response => {
              this.multiline_mo_val = response.data.data;
           })
           .catch(error => {
             console.log(error);
           })

      axios.get(endpoint_a)
           .then(response => {
             this.housing_summary = response.data.data;
           })
           .catch(error => {
             console.log(error);
           })
    },
    onProvinceChange: function(province) {
      if(province) {
        this.province = this.barrios[province.b_id];
        this.getImportance(this.province.id, 2016);

        this.vw = 'overview';
        this.h_kind = 'purchase';
        this.getMonthly(this.h_kind);
      } else {
        this.province = undefined;
      }
    }
  },
  mounted: function() {
    this.$on('province-chosen', this.onProvinceChange);
    // Initial map coloring
    this.getBarrios();
    this.getBarriosVal('/api/property/us_val/avg/');
    this.getHeatmapVal('/api/humanity/elderly_care');
  }
});
