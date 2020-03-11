stylus:
	cd src && ../lib/node_modules/stylus/bin/stylus -m --include ../lib/node_modules -u jeet -u axis -u autoprefixer-stylus -u rupture stylus/*.styl -o ../assets/css/ -w
html:
	cd src && ../lib/node_modules/pug-cli/index.js -P -w pug/*.pug -o ../
reinstall:
	cd lib && npm install --save-dev npm fs tls net module deps-ok stylus rupture pug-cli pug jeet axis autoprefixer segment-js postcss-cli material-components-web jquery @mdi/font @mdi/js @mdi/svg @mdi/util webpack webpack-cli extract-text-webpack-plugin file-loader css-loader style-loader @babel/core
install:
	cd lib && npm install --save-dev
zip:
	zip -r default_template.zip ./
