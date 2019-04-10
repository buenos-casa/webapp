// Include libraries
import Vue from 'vue'
import axios from 'axios'
import WebFont from 'webfontloader'
import Mapbaires from '../components/mapbaires.vue'

// Init Google Fonts
WebFont.load({
  google: {
    families: ['Open+Sans:300,400']
  }
})

// Init Vue app
const vue_app = new Vue({
  el: '#app',
  components: {
    Mapbaires
  }
});
