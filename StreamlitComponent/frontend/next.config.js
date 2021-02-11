// https://github.com/kutlugsahin/next-transpile-modules
// pass the modules you would like to see transpiled
const withTM = require('next-transpile-modules')(['streamlit-component-lib']);
module.exports = withTM();