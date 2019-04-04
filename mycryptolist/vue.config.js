const BundleTracker = require("webpack-bundle-tracker");
// const webpack = require("webpack");

module.exports = {
    publicPath: "http://0.0.0.0:8081/",
    outputDir: './dist/',


    chainWebpack: config => {

        config.optimization
            .splitChunks(false)

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: '../mycryptolist/webpack-stats.json'}])

        config.resolve.alias
            .set('__STATIC__', 'static')

        config.devServer
            .public('http://0.0.0.0:8081')
            .host('0.0.0.0')
            .port(8081)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
            }
        };

// new webpack.ProvidePlugin({
//     $: 'jquery',
//     jquery: 'jquery',
//     'window.jQuery': 'jquery',
//     jQuery: 'jquery'
//   });