# Material Design Icons - Util

Utility methods for Material Design Icons' Build scripts.

## Getting Started

The `@mdi/util` package relies on the `@mdi/svg` package. Any version of `@mdi/svg` can be used.

```
npm install @mdi/svg @mdi/util
```

- getVersion()
- getMeta([bool withPaths])
- write(file, data)
- read(file)
- exists(file)

### getVersion()

This returns the version of `@mdi/svg` referenced in the `package.json`.

**returns** semver string `major.minor.build`

### getMeta([bool withPaths])

The main use of this library is to get all the icon data from the `meta.json`. Since the `meta.json` does not contain the SVG path data this method optionally allows this to be added to the object.

Please reference [meta.json](https://github.com/Templarian/MaterialDesign-SVG/blob/master/meta.json) for more information.

**returns** icon array []

### write(file, data)

```
import { write } from '@mdi/util'

write('file.txt', 'Hello World!')
```

### read(file)

```
import { read } from '@mdi/util'

const foo = read('file.txt')
```

**returns** string of file contents

### exists(file)

```
import { exists } from '@mdi/util'

if (exits('file.txt')) {
    // file exists!
}
```

**returns** bool `true`/`false` if file exists
