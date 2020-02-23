const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = (env, argv) => {
    const DEV = argv ? argv.mode === 'development' : true;
    if (DEV) console.log(`Webpack running in DEVELOPMENT mode`);
    else console.log(`Webpack running in PRODUCTION mode`);

    return {
        entry: {
            app: './js/app.ts',
            lib: './js/lib.js',
            styles: './styles/main.sass',
        },
        output: {
            path: path.resolve(__dirname, './dist/webpack'),
            publicPath: '/static/',
            filename: DEV ? "[name].js" : '[name].[chunkhash].js',
        },
        optimization: {
            // TODO: Can't do this with current django-webpack-loader. There is a fork to do this but will leave
            //       until we have a large enough app to make it worth it.
            //       See: https://github.com/owais/webpack-bundle-tracker/pull/41#issuecomment-463709521
            // splitChunks: {
            //     chunks: 'all',
            // },
        },
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    loader: 'vue-loader',
                },

                {
                    test: /\.([tj])s$/,
                    use: [
                        'babel-loader',
                    ],
                    exclude: /node_modules/,
                },
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                            options: {
                                hmr: DEV,
                            },
                        },
                        {loader: 'css-loader', options: {importLoaders: 1}},
                        'postcss-loader',
                        {
                            loader: 'sass-loader',
                            options: {
                                sassOptions: {
                                    indentedSyntax: true
                                },
                            }
                        }
                    ],
                },
                {
                    test: /\.(png|jpe?g|gif|svg|ttf|eot|woff2?)$/i,
                    use: [
                        {
                            loader: 'file-loader',
                        },
                    ],
                },
            ]

        },
        resolve: {
            extensions: ['.ts', '.js', '.vue', '.json'],
            alias: {
                'assets': path.resolve(__dirname, 'assets'),
                'vue$': 'vue/dist/vue.esm.js',
            }
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: DEV ? "[name].css" : "[name].[chunkhash].css"
            }),
            new BundleTracker({
                filename: 'dist/webpack-stats.json'
            }),
            new VueLoaderPlugin(),
        ],
        devtool: DEV ? '#eval-source-map' : '#source-map',
        performance: {
            hints: 'warning'
        },
    }
};
