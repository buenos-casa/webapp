const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');

module.exports = {
  entry: {
    'js/script.min.js': './static/assets/js/script.js',
    'css/style.min.css': './static/assets/scss/style.scss',
    'components/mapgeojson.min.vue': './static/assets/components/mapgeojson.vue',
    'components/multiline.min.vue': './static/assets/components/multiline.vue'
  },
  output: {
    path: path.resolve(__dirname, 'static'),
    filename: '[name]'
  },
  module: {
    loaders: [
      {
        test: /\.js$/, 
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ['@babel/preset-env']
        }
      },
      {
        test: /\.(css|scss)$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            {
              loader: 'css-loader',
              options: {
                minimize: true
              }
            },
            {loader: 'postcss-loader'},
            {loader: 'sass-loader'}
          ]
        })
      },
      {
        test: /\.vue$/,
        loader: "vue-loader",
        options: {
          loaders: {
            scss: 'vue-style-loader!css-loader!sass-loader'
          }
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  },
  plugins: [
    new ExtractTextPlugin('[name]'),
    new webpack.LoaderOptionsPlugin({
      vue: {
        loaders: {
          scss: 'style!css!scss'
        }
      }
    })//,
    //new BrowserSyncPlugin({
      // browse to http://localhost:3000/ during development,
      // ./public directory is being served
      //host: 'localhost',
      //port: 8000,
      //server: { baseDir: ['public'] }
    //})
  ]
}
