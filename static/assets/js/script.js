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
    Mapgeojson
  }
});
