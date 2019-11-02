const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = (env, argv) => {
    const DEV = argv.mode === 'development';
    if (DEV) console.log(`Webpack running in DEVELOPMENT mode`);
    else console.log(`Webpack running in PRODUCTION mode`);

    return {
        entry: {
            app: './js/app.js',
            lib: './js/lib.js',
            styles: './styles/main.sass',
        },
        output: {
            path: path.resolve(__dirname, './dist/webpack'),
            publicPath: '/static/',
            filename: DEV ? "[name].js" : '[name].[chunkhash].js',
        },
        module: {
            rules: [
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                            options: {
                                hmr: DEV,
                            },
                        },
                        'css-loader',
                        // postcss-loader
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
            extensions: ['.js', '.json'],
            alias: {
                'assets': path.resolve(__dirname, 'assets'),
            }
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: DEV ? "[name].css" : "[name].[chunkhash].css"
            }),
            new BundleTracker({
                filename: 'dist/webpack-stats.json'
            })
        ],
        devtool: DEV ? '#eval-source-map' : '#source-map',
        performance: {
            hints: 'warning'
        },
    }
};
