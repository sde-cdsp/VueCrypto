const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    publicPath: "http://localhost:8001/",
    outputDir: './dist/',
    filenameHashing: false,
    devServer: {
        hotOnly: true,
        port: 8001,
        headers: { // allow different CORS headers
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Credentials': true,
        },
    },
    configureWebpack: {
        resolve: {alias: {'__STATIC__': 'static'}},
        plugins: [new BundleTracker({filename: './webpack-stats.json'})],
    },
    chainWebpack: config => {
        config.optimization.delete('splitChunks');
    }
};