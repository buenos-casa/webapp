// Include libraries
import Vue from 'vue'
import axios from 'axios'
import WebFont from 'webfontloader'
import Mapgeojson from '../components/mapgeojson.vue'
import Multiline from '../components/multiline.vue'
import {
  // Basic
  d3Pie,
  d3Line,
  d3MultiLine,
  d3HorizontalBar,
  d3VerticalBar,
  d3Circle,
  d3Metric,

  // Functional
  d3HorizontalSlider,
  d3VerticalSlider,
} from 'd3-vs';

console.log('It\'s running!');


// Init Vue app
const vue_app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  components: {
    Mapgeojson,
    // TODO: Multiline,
    d3Pie,
    d3Circle,
    d3Line,
    d3MultiLine,
    d3HorizontalBar,
    d3Metric
  },
  data() {
    return {
      vw: 'overview',
      st: 'pv',
      h_kind: 'purchase',
      barrios: undefined,
      barriocensus: {"own": 0.57, "rent": 0.18, "uinhab": 0.25},
      opened: false,
      census: [],
      barrios_val: [],
      heatmap_val: [],
      importance_val: [],
      multiline_mo_val: [],
      housing_summary: undefined,
      province: undefined,
      month_sell: [],
      sell_data: []
    }
  },
  methods: {
    getBarrios() {
      axios.get('/api/barrio/')
           .then(response => {
             this.barrios = response.data.data;
             console.log(this.barrios);
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
    getBarrioCensus(barrio) {
      // If the barrio has been set
      if(barrio !== undefined) {
        axios.get('/api/census/barrio/' + barrio)
          .then(response => {
            this.barriocensus = response.data.data;
          })
          .catch(error => {
            console.log(error);
          })
      } else {
        // Overall buenos aires stats
        this.barriocensus = {"own": 0.57, "rent": 0.18, "uinhab": 0.08};
      }
    },
    getMonthly(kind) {
      var endpoint = undefined;
      var endpoint_a = undefined;
      if(this.province) {
        endpoint = '/api/' + kind + '/monthly/' + this.province.id;
        endpoint_a = '/api/' + kind + '/' + this.province.id;
      } else {
        endpoint = '/api/' + kind + '/monthly/all';
        endpoint_a = '/api/' + kind + '/all';
      }
      axios.get(endpoint)
           .then(response => {
              this.month_sell = response.data.data;

              for(let i = 0; i < this.month_sell.length; i++){
                this.month_sell[i].key = new Date(this.month_sell[i].key);
              }
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
        // Get object from barrios list
        this.province = this.barrios[province.b_id];
        // Update the montly sell data
        this.getMonthly('purchase');
        // Update importance graph
        this.getImportance(this.province.id, 2016);

        this.vw = 'overview';
        this.h_kind = 'purchase';
        this.getMonthly(this.h_kind);
        this.getBarrioCensus(this.province.id);
      } else {
        this.province = undefined;
        this.getBarrioCensus(undefined);
      }
    },
    toggleCard: function(){
      return {}
    }
  },
  mounted: function() {
    this.$on('province-chosen', this.onProvinceChange);
    // Initial map coloring
    this.getBarrios();
    this.getBarrioCensus(undefined);
    this.getBarriosVal('/api/property/us_val/avg/');
    this.getHeatmapVal('/api/humanity/elderly_care');
  }
});
