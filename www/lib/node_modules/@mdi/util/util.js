const fs = require('fs');

const encoding = "utf8";
const folder = `${__dirname}/../`;
const packageName = 'svg'

const getVersion = (overridePackageName) => {
  const pName = overridePackageName || packageName;
  const file = fs.readFileSync(`${folder}${pName}/package.json`, { encoding });
  return JSON.parse(file).version;
};

const getMeta = (withPaths, overridePackageName) => {
  const pName = overridePackageName || packageName;
  const file = fs.readFileSync(`${folder}${pName}/meta.json`, { encoding });
  const meta = JSON.parse(file);
  if (withPaths) {
    const total = meta.length;
    meta.forEach((icon, i) => {
      const svg = fs.readFileSync(`${folder}${pName}/svg/${icon.name}.svg`, { encoding });
      icon.path = svg.match(/ d="([^"]+)"/)[1];
    });
  }
  return meta;
};

exports.getVersionLight = () => {
  return getVersion('light-svg');
}

exports.getMetaLight = (withPaths) => {
  return getMeta(withPaths, 'light-svg');
}

exports.getVersion = getVersion;

exports.getMeta = getMeta;

exports.closePath = (path) => {
  return path.replace(/(\d)M/g, '$1ZM');
};

exports.write = (file, data) => {
  fs.writeFileSync(file, data);
};

exports.read = (file) => {
  fs.readFileSync(file);
};

exports.exists = (file) => {
  return fs.exists(file);
};
