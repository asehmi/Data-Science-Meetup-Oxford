// https://github.com/kutlugsahin/next-transpile-modules
const withTM = require('next-transpile-modules')(['streamlit-component-lib']); // pass the modules you would like to see transpiled
 
module.exports = withTM();