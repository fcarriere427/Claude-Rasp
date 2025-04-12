module.exports = {
  publicPath: '/',
  configureWebpack: {
    devtool: 'source-map'
  },
  // Assurer que favicon.ico et autres assets sont correctement copiés
  chainWebpack: config => {
    config.plugin('copy')
      .tap(args => {
        args[0].patterns.push({
          from: 'public/favicon.ico',
          to: 'favicon.ico'
        });
        return args;
      });
  }
}
