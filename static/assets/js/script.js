// Include libraries
import Vue from 'vue'
import axios from 'axios'
import Mapgeojson from '../components/mapgeojson.vue'
import Multiline from '../components/multiline.vue'
import Barrio from '../components/barrio.vue'
import {
  // Basic
  d3Metric,
  d3Pie,
  d3Line,
  d3MultiLine,
  d3HorizontalBar,
  d3Circle,

} from 'd3-vs';

console.log('It\'s running!');


// Init Vue app
const vue_app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  components: {
    Mapgeojson,
    Barrio,
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
      igy: '2015',
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
      sell_data: [],
      health_stats: [],
      sports_stats: [],
      humanity_stats: [],
      culture_stats: [],
      mislabelled: []
    }
  },
  computed: {
    getMislabelledCount: function() {
      var count = new Array();

      var filled_per = 0.0;

      for(let i = 0; i < this.barrios.length; i++) {
        var vl = this.mislabelled.reduce((acc, cur) => cur.data.misclass_as === i ? ++acc : acc, 0) / this.mislabelled.length;
        vl = Math.round(vl * 100) / 100
        if(vl > 0.01) {
          filled_per += vl;
          count.push(
            {
              key: this.barrios[i].name,
              value: vl > 0.05 ? vl : 0,
            }
          );
        }
      }

      if(filled_per <= 1.0) {
        count.push(
          {
            key: 'Other',
            value: Math.round((1 - filled_per) * 100) / 100
          }
        );
      }

      count.sort((a,b) => a.value - b.value);

      count.reverse();

      console.log(count);

      return count;
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
    getBasicStats(){
      var health_endpoint = '/api/health/all';
      var sports_endpoint = '/api/sports/all';
      var humanity_endpoint = '/api/humanity/all';
      var culture_endpoint = '/api/culture/all';
      
      
      axios.get(health_endpoint)
      .then(response => {
        this.health_stats = response.data.data;
        console.log('Health Data: ' + this.health_stats);
      })
      .catch(error => {
        console.log(error);
      });

      axios.get(sports_endpoint)
      .then(response => {
        this.sports_stats = response.data.data;
        console.log('Sports Data: ' + this.sports_stats);
      })
      .catch(error => {
        console.log(error);
      });

      axios.get(humanity_endpoint)
      .then(response => {
        this.humanity_stats = response.data.data;
      })
      .catch(error => {
        console.log(error);
      });

      axios.get(culture_endpoint)
      .then(response => {
        this.culture_stats = response.data.data;
      })
      .catch(error => {
        console.log(error);
      });

    },
    getMislabelled: function(barrio) {
      var endpoint = 'api/misclassified/' + barrio + '/points';
      axios.get(endpoint)
           .then(response => {
             this.mislabelled = response.data.data;
             console.log(this.mislabelled);
           })
           .catch(error => {
            console.log(error); 
           });
    },
    onProvinceChange: function(province) {
      if(province) {
        // Get object from barrios list
        this.province = this.barrios[province.b_id];
        this.getBarrioCensus(this.province.id);
        if(this.vw === 'overview') {
          //this.vw = 'overview';
          this.h_kind = 'purchase';
          this.getMonthly(this.h_kind);
        } else if(this.vw === 'analysis') {
          // Update analytics
          this.getMislabelled(this.province.id);
          this.getImportance(this.province.id, this.igy); 
        }
      } else {
        this.province = undefined;
        this.getBarrioCensus(undefined);
      }
    }
  },
  mounted: function() {
    this.$on('province-chosen', this.onProvinceChange);
    // Initial map coloring
    this.getBarrios();
    this.getBarrioCensus(undefined);
    this.getBasicStats();
    this.getBarriosVal('/api/property/us_val/avg/');
    this.getHeatmapVal('/api/humanity/elderly_care');
  }
});
